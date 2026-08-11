import json
import urllib.request
import urllib.parse
import time
import re
import sys
import concurrent.futures
import threading

# Country/nationality to ISO 2-letter code mapping
NATIONALITY_MAP = {
    'american': 'us', 'united states': 'us', 'u.s.': 'us', 'usa': 'us',
    'british': 'gb', 'english': 'gb', 'scottish': 'gb', 'welsh': 'gb', 'united kingdom': 'gb', 'england': 'gb', 'scotland': 'gb', 'wales': 'gb', 'uk': 'gb',
    'canadian': 'ca', 'canada': 'ca',
    'australian': 'au', 'australia': 'au',
    'french': 'fr', 'france': 'fr',
    'german': 'de', 'germany': 'de',
    'italian': 'it', 'italy': 'it',
    'spanish': 'es', 'spain': 'es',
    'portuguese': 'pt', 'portugal': 'pt',
    'dutch': 'nl', 'netherlands': 'nl', 'holland': 'nl', 'surinamese-dutch': 'nl',
    'belgian': 'be', 'belgium': 'be',
    'swedish': 'se', 'sweden': 'se',
    'norwegian': 'no', 'norway': 'no',
    'danish': 'dk', 'denmark': 'dk',
    'finnish': 'fi', 'finland': 'fi',
    'icelandic': 'is', 'iceland': 'is',
    'irish': 'ie', 'ireland': 'ie',
    'polish': 'pl', 'poland': 'pl',
    'czech': 'cz', 'czech republic': 'cz', 'czechia': 'cz',
    'slovak': 'sk', 'slovakia': 'sk', 'slovakian': 'sk',
    'hungarian': 'hu', 'hungary': 'hu',
    'romanian': 'ro', 'romania': 'ro',
    'bulgarian': 'bg', 'bulgaria': 'bg',
    'serbian': 'rs', 'serbia': 'rs',
    'croatian': 'hr', 'croatia': 'hr',
    'slovenian': 'si', 'slovenia': 'si',
    'bosnian': 'ba', 'bosnia': 'ba',
    'greek': 'gr', 'greece': 'gr',
    'turkish': 'tr', 'turkey': 'tr', 'türkiye': 'tr',
    'russian': 'ru', 'russia': 'ru',
    'ukrainian': 'ua', 'ukraine': 'ua',
    'japanese': 'jp', 'japan': 'jp',
    'south korean': 'kr', 'korean': 'kr', 'south korea': 'kr',
    'chinese': 'cn', 'china': 'cn',
    'taiwanese': 'tw', 'taiwan': 'tw',
    'indian': 'in', 'india': 'in',
    'thai': 'th', 'thailand': 'th',
    'vietnamese': 'vn', 'vietnam': 'vn',
    'filipino': 'ph', 'philippines': 'ph', 'philippine': 'ph', 'pinoy': 'ph',
    'indonesian': 'id', 'indonesia': 'id',
    'malaysian': 'my', 'malaysia': 'my',
    'singaporean': 'sg', 'singapore': 'sg',
    'mexican': 'mx', 'mexico': 'mx',
    'colombian': 'co', 'colombia': 'co',
    'brazilian': 'br', 'brazil': 'br',
    'argentine': 'ar', 'argentinian': 'ar', 'argentina': 'ar',
    'chilean': 'cl', 'chile': 'cl',
    'peruvian': 'pe', 'peru': 'pe',
    'venezuelan': 've', 'venezuela': 've',
    'cuban': 'cu', 'cuba': 'cu',
    'dominican': 'do', 'dominican republic': 'do',
    'puerto rican': 'pr', 'puerto rico': 'pr',
    'panamanian': 'pa', 'panama': 'pa',
    'paraguayan': 'py', 'paraguay': 'py',
    'ecuadorian': 'ec', 'ecuador': 'ec',
    'south african': 'za', 'south africa': 'za',
    'nigerian': 'ng', 'nigeria': 'ng',
    'kenyan': 'ke', 'kenya': 'ke',
    'egyptian': 'eg', 'egypt': 'eg',
    'moroccan': 'ma', 'morocco': 'ma',
    'algerian': 'dz', 'algeria': 'dz',
    'tunisian': 'tn', 'tunisia': 'tn',
    'saudi': 'sa', 'saudi arabian': 'sa', 'saudi arabia': 'sa',
    'emirati': 'ae', 'uae': 'ae', 'united arab emirates': 'ae',
    'lebanese': 'lb', 'lebanon': 'lb',
    'israeli': 'il', 'israel': 'il',
    'new zealand': 'nz', 'new zealander': 'nz',
    'lithuanian': 'lt', 'lithuania': 'lt',
    'latvian': 'lv', 'latvia': 'lv',
    'estonian': 'ee', 'estonia': 'ee',
    'albanian': 'al', 'albania': 'al', 'kosovar': 'xk', 'kosovo': 'xk', 'kosovan': 'xk',
    'montenegrin': 'me', 'montenegro': 'me',
    'north macedonian': 'mk', 'north macedonia': 'mk',
    'austrian': 'at', 'austria': 'at',
    'swiss': 'ch', 'switzerland': 'ch',
    'congolese': 'cd', 'congo': 'cd',
    'ghanaian': 'gh', 'ghana': 'gh',
    'iraqi': 'iq', 'iraq': 'iq',
    'iranian': 'ir', 'iran': 'ir', 'persian': 'ir',
    'pakistani': 'pk', 'pakistan': 'pk',
    'jamaican': 'jm', 'jamaica': 'jm',
    'uruguayan': 'uy', 'uruguay': 'uy',
    'bolivian': 'bo', 'bolivia': 'bo',
    'costa rican': 'cr', 'costa rica': 'cr',
}

CITY_COUNTRY = {
    'london': 'gb', 'manchester': 'gb', 'birmingham': 'gb', 'bristol': 'gb', 'liverpool': 'gb', 'leeds': 'gb', 'sheffield': 'gb', 'nottingham': 'gb', 'glasgow': 'gb', 'edinburgh': 'gb',
    'new york': 'us', 'los angeles': 'us', 'chicago': 'us', 'houston': 'us', 'atlanta': 'us', 'miami': 'us', 'detroit': 'us', 'philadelphia': 'us', 'dallas': 'us', 'san francisco': 'us', 'seattle': 'us', 'boston': 'us', 'brooklyn': 'us', 'compton': 'us', 'harlem': 'us', 'queens': 'us', 'bronx': 'us', 'oakland': 'us', 'memphis': 'us', 'new orleans': 'us', 'nashville': 'us', 'denver': 'us', 'portland': 'us', 'pittsburgh': 'us', 'cleveland': 'us', 'baltimore': 'us', 'washington': 'us', 'las vegas': 'us', 'san diego': 'us', 'phoenix': 'us', 'austin': 'us', 'minneapolis': 'us',
    'paris': 'fr', 'marseille': 'fr', 'lyon': 'fr', 'toulouse': 'fr', 'nice': 'fr', 'nantes': 'fr', 'strasbourg': 'fr', 'bordeaux': 'fr', 'lille': 'fr', 'seine-saint-denis': 'fr',
    'berlin': 'de', 'hamburg': 'de', 'munich': 'de', 'cologne': 'de', 'frankfurt': 'de', 'düsseldorf': 'de', 'stuttgart': 'de',
    'rome': 'it', 'milan': 'it', 'naples': 'it', 'turin': 'it', 'florence': 'it', 'genoa': 'it', 'bologna': 'it', 'palermo': 'it',
    'madrid': 'es', 'barcelona': 'es', 'seville': 'es', 'valencia': 'es', 'bilbao': 'es',
    'lisbon': 'pt', 'porto': 'pt',
    'amsterdam': 'nl', 'rotterdam': 'nl', 'the hague': 'nl', 'utrecht': 'nl',
    'brussels': 'be', 'antwerp': 'be',
    'stockholm': 'se', 'gothenburg': 'se', 'malmö': 'se',
    'oslo': 'no', 'bergen': 'no', 'trondheim': 'no',
    'copenhagen': 'dk', 'aarhus': 'dk',
    'helsinki': 'fi', 'espoo': 'fi', 'tampere': 'fi',
    'dublin': 'ie', 'cork': 'ie', 'mullingar': 'ie',
    'warsaw': 'pl', 'kraków': 'pl', 'krakow': 'pl', 'wrocław': 'pl', 'gdańsk': 'pl', 'poznań': 'pl', 'katowice': 'pl',
    'prague': 'cz', 'brno': 'cz',
    'bratislava': 'sk', 'košice': 'sk',
    'budapest': 'hu',
    'bucharest': 'ro', 'cluj': 'ro',
    'sofia': 'bg', 'plovdiv': 'bg',
    'belgrade': 'rs', 'novi sad': 'rs',
    'zagreb': 'hr',
    'athens': 'gr', 'thessaloniki': 'gr',
    'istanbul': 'tr', 'ankara': 'tr', 'izmir': 'tr',
    'moscow': 'ru', 'saint petersburg': 'ru',
    'kyiv': 'ua', 'kiev': 'ua', 'kharkiv': 'ua', 'odesa': 'ua',
    'tokyo': 'jp', 'osaka': 'jp',
    'seoul': 'kr', 'busan': 'kr',
    'beijing': 'cn', 'shanghai': 'cn', 'hong kong': 'hk',
    'taipei': 'tw', 'kaohsiung': 'tw',
    'mumbai': 'in', 'delhi': 'in', 'bangalore': 'in', 'hyderabad': 'in', 'chennai': 'in', 'kolkata': 'in', 'pune': 'in',
    'bangkok': 'th',
    'hanoi': 'vn', 'ho chi minh city': 'vn',
    'manila': 'ph', 'quezon city': 'ph',
    'jakarta': 'id', 'surabaya': 'id',
    'kuala lumpur': 'my',
    'singapore': 'sg',
    'mexico city': 'mx', 'guadalajara': 'mx', 'monterrey': 'mx', 'culiacán': 'mx', 'culiacan': 'mx', 'sinaloa': 'mx',
    'bogotá': 'co', 'bogota': 'co', 'medellín': 'co', 'medellin': 'co', 'cali': 'co',
    'são paulo': 'br', 'rio de janeiro': 'br',
    'buenos aires': 'ar',
    'santiago': 'cl',
    'lima': 'pe',
    'caracas': 've', 'maracaibo': 've',
    'havana': 'cu',
    'santo domingo': 'do',
    'johannesburg': 'za', 'cape town': 'za', 'durban': 'za', 'pretoria': 'za', 'soweto': 'za',
    'lagos': 'ng', 'abuja': 'ng',
    'nairobi': 'ke',
    'cairo': 'eg', 'alexandria': 'eg',
    'casablanca': 'ma', 'rabat': 'ma', 'marrakech': 'ma', 'fez': 'ma',
    'riyadh': 'sa', 'jeddah': 'sa',
    'dubai': 'ae', 'abu dhabi': 'ae',
    'beirut': 'lb',
    'tel aviv': 'il', 'jerusalem': 'il',
    'auckland': 'nz', 'wellington': 'nz',
    'vilnius': 'lt', 'kaunas': 'lt',
    'riga': 'lv',
    'tallinn': 'ee',
    'tirana': 'al',
    'vienna': 'at', 'salzburg': 'at',
    'zurich': 'ch', 'geneva': 'ch',
    'toronto': 'ca', 'montreal': 'ca', 'vancouver': 'ca',
    'sydney': 'au', 'melbourne': 'au', 'brisbane': 'au',
    'kingston': 'jm',
    'accra': 'gh',
    'reykjavík': 'is', 'reykjavik': 'is',
}


def extract_nationality(text):
    """Extract nationality/country from Wikipedia extract text."""
    if not text:
        return None, None
    
    text_lower = text.lower()
    first_sentences = '. '.join(text.split('.')[:3]).lower()
    
    # Pattern 1: "is a/an [nationality] [profession]"
    pattern1 = re.findall(
        r'is (?:a|an) ([A-Za-z\-\s]+?)[\s\-]+(?:singer|rapper|musician|band|group|artist|songwriter|producer|DJ|dj|composer|vocalist|entertainer|record producer|hip hop|pop|rock|electronic|musical|music|recording|hip-hop|indie|alternative|dance|punk|metal|rap|trap|drill|grime|k-pop|j-pop|duo|trio|collective|ensemble|orchestra|act|solo)',
        text, re.IGNORECASE
    )
    if pattern1:
        for match in pattern1:
            match_clean = match.strip().lower()
            # Try full match
            if match_clean in NATIONALITY_MAP:
                return NATIONALITY_MAP[match_clean], f"matched '{match.strip()}'"
            # Try individual words (last word first, as it's usually the nationality)
            words = match_clean.split()
            for w in reversed(words):
                if w in NATIONALITY_MAP:
                    return NATIONALITY_MAP[w], f"word match '{w}'"
    
    # Pattern 2: "born in [city/country]" or "from [city/country]"
    pattern2 = re.findall(
        r'(?:born|raised|based|originating) in ([A-Za-zÀ-ÿ\s\-\.\,\']+?)(?:\.|,|\)|who| is| and)',
        first_sentences, re.IGNORECASE
    )
    if pattern2:
        for match in pattern2:
            parts = [p.strip().lower() for p in match.split(',')]
            for part in reversed(parts):
                if part in NATIONALITY_MAP:
                    return NATIONALITY_MAP[part], f"born/from '{part}'"
                if part in CITY_COUNTRY:
                    return CITY_COUNTRY[part], f"city '{part}'"
    
    # Pattern 3: "from [place]"
    pattern3 = re.findall(
        r'from ([A-Za-zÀ-ÿ\s\-\.\,\']+?)(?:\.|,|\)|who| is| and| that)',
        first_sentences, re.IGNORECASE
    )
    if pattern3:
        for match in pattern3:
            parts = [p.strip().lower() for p in match.split(',')]
            for part in reversed(parts):
                if part in NATIONALITY_MAP:
                    return NATIONALITY_MAP[part], f"from '{part}'"
                if part in CITY_COUNTRY:
                    return CITY_COUNTRY[part], f"from city '{part}'"
    
    # Pattern 4: Check for nationality words in first sentences (longer matches first)
    sorted_nationalities = sorted(NATIONALITY_MAP.keys(), key=len, reverse=True)
    for nat in sorted_nationalities:
        if len(nat) < 4:
            continue
        if nat in first_sentences:
            idx = first_sentences.find(nat)
            before = first_sentences[idx-1] if idx > 0 else ' '
            after = first_sentences[idx+len(nat)] if idx+len(nat) < len(first_sentences) else ' '
            if not before.isalpha() and not after.isalpha():
                return NATIONALITY_MAP[nat], f"found '{nat}' in intro"
    
    # Pattern 5: Check cities in first sentences
    sorted_cities = sorted(CITY_COUNTRY.keys(), key=len, reverse=True)
    for city in sorted_cities:
        if len(city) < 4:
            continue
        if city in first_sentences:
            idx = first_sentences.find(city)
            before = first_sentences[idx-1] if idx > 0 else ' '
            after = first_sentences[idx+len(city)] if idx+len(city) < len(first_sentences) else ' '
            if not before.isalpha() and not after.isalpha():
                return CITY_COUNTRY[city], f"city '{city}' in intro"
    
    return None, None


def fetch_url(url):
    """Fetch a URL with timeout."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'VizConValidation/1.0 (research project)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return None


def query_wikipedia_direct(artist_name):
    """Query Wikipedia API directly by title."""
    encoded_name = urllib.parse.quote(artist_name)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded_name}&prop=extracts&exintro=true&format=json&explaintext=true&redirects=1"
    data = fetch_url(url)
    if data:
        pages = data.get('query', {}).get('pages', {})
        for page_id, page in pages.items():
            if page_id != '-1' and 'extract' in page and page['extract'].strip():
                return page['extract'], page.get('title', '')
    return None, None


def query_wikipedia_search(artist_name):
    """Search Wikipedia for the artist."""
    encoded_name = urllib.parse.quote(artist_name)
    search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded_name}&limit=5&format=json"
    data = fetch_url(search_url)
    if data and len(data) > 1 and data[1]:
        music_keywords = ['singer', 'rapper', 'musician', 'band', 'group', 'artist', 'songwriter', 'producer', 'dj', 'album', 'single', 'song', 'music', 'hip hop', 'pop', 'rock', 'record', 'vocal', 'genre', 'label', 'track', 'rapper', 'mc', 'feat']
        for title in data[1][:3]:
            encoded_title = urllib.parse.quote(title)
            detail_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded_title}&prop=extracts&exintro=true&format=json&explaintext=true&redirects=1"
            detail = fetch_url(detail_url)
            if detail:
                pages = detail.get('query', {}).get('pages', {})
                for page_id, page in pages.items():
                    if page_id != '-1' and 'extract' in page and page['extract'].strip():
                        extract = page['extract'].lower()
                        if any(kw in extract for kw in music_keywords):
                            return page['extract'], title
            time.sleep(0.1)
    return None, None


def lookup_artist(artist_entry):
    """Look up a single artist on Wikipedia."""
    full_name = artist_entry['name']
    our_country = artist_entry['our_country']
    lookup_name = full_name.split('|')[0].strip()
    
    # Try direct lookup
    extract, wiki_title = query_wikipedia_direct(lookup_name)
    
    # If not found or not music-related, try with suffixes
    if not extract:
        suffixes = [' (singer)', ' (rapper)', ' (musician)', ' (band)', ' (DJ)', ' (group)']
        for suffix in suffixes:
            extract, wiki_title = query_wikipedia_direct(lookup_name + suffix)
            if extract:
                break
            time.sleep(0.1)
    
    # If still not found, try search
    if not extract:
        extract, wiki_title = query_wikipedia_search(lookup_name)
    
    if extract:
        country_code, note = extract_nationality(extract)
        if country_code:
            match = (country_code == our_country)
            return {
                'name': full_name,
                'our_country': our_country,
                'wiki_country': country_code,
                'match': match,
                'wiki_note': f"{note} (wiki: {wiki_title})"
            }
        else:
            return {
                'name': full_name,
                'our_country': our_country,
                'wiki_country': 'unknown',
                'match': None,
                'wiki_note': f"Wikipedia page found ({wiki_title}) but no nationality extracted"
            }
    else:
        return {
            'name': full_name,
            'our_country': our_country,
            'wiki_country': 'unknown',
            'match': None,
            'wiki_note': 'No Wikipedia page found'
        }


def main():
    input_path = '/Users/gabmc/Library/CloudStorage/OneDrive-amazon.com/4. Claude/vizcon-project/data/validation_sample_100.json'
    output_path = '/Users/gabmc/Library/CloudStorage/OneDrive-amazon.com/4. Claude/vizcon-project/data/validation_results_100.json'
    
    with open(input_path, 'r', encoding='utf-8') as f:
        artists = json.load(f)
    
    total = len(artists)
    results = []
    
    # Process sequentially with minimal delay (Wikipedia rate limit is generous)
    for i, artist in enumerate(artists):
        lookup_name = artist['name'].split('|')[0].strip()
        print(f"[{i+1}/{total}] {lookup_name}...", end=' ', flush=True)
        
        result = lookup_artist(artist)
        results.append(result)
        
        if result['wiki_country'] == 'unknown':
            print(f"-> NOT FOUND ({result['wiki_note'][:50]})", flush=True)
        elif result['match']:
            print(f"-> MATCH ({result['wiki_country']})", flush=True)
        else:
            print(f"-> MISMATCH ours={result['our_country']} wiki={result['wiki_country']} ({result['wiki_note'][:60]})", flush=True)
        
        time.sleep(0.2)  # Minimal rate limiting
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    found = [r for r in results if r['wiki_country'] != 'unknown']
    not_found = [r for r in results if r['wiki_country'] == 'unknown']
    matches = [r for r in found if r['match'] == True]
    mismatches = [r for r in found if r['match'] == False]
    
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total artists checked: {total}")
    print(f"Wikipedia found (with nationality): {len(found)}")
    print(f"Wikipedia not found / no nationality: {len(not_found)}")
    print(f"Matches: {len(matches)}")
    print(f"Mismatches: {len(mismatches)}")
    if found:
        accuracy = len(matches) / len(found) * 100
        print(f"Accuracy: {len(matches)}/{len(found)} = {accuracy:.1f}%")
    
    if mismatches:
        print(f"\nMISMATCHES ({len(mismatches)}):")
        print("-"*60)
        for r in mismatches:
            print(f"  {r['name']}: ours={r['our_country']}, wiki={r['wiki_country']} | {r['wiki_note']}")
    
    if not_found:
        print(f"\nNOT FOUND / NO NATIONALITY ({len(not_found)}):")
        print("-"*60)
        for r in not_found:
            print(f"  {r['name']} (assigned: {r['our_country']}) - {r['wiki_note'][:60]}")


if __name__ == '__main__':
    main()

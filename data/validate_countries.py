import json
import urllib.request
import urllib.parse
import time
import re
import sys

# Country/nationality to ISO 2-letter code mapping
NATIONALITY_MAP = {
    # Common nationalities
    'american': 'us', 'united states': 'us', 'u.s.': 'us', 'usa': 'us',
    'british': 'gb', 'english': 'gb', 'scottish': 'gb', 'welsh': 'gb', 'united kingdom': 'gb', 'england': 'gb', 'scotland': 'gb', 'wales': 'gb', 'london': 'gb', 'uk': 'gb',
    'canadian': 'ca', 'canada': 'ca',
    'australian': 'au', 'australia': 'au',
    'french': 'fr', 'france': 'fr', 'paris': 'fr', 'marseille': 'fr',
    'german': 'de', 'germany': 'de', 'berlin': 'de',
    'italian': 'it', 'italy': 'it', 'milan': 'it', 'rome': 'it', 'naples': 'it',
    'spanish': 'es', 'spain': 'es', 'madrid': 'es', 'barcelona': 'es',
    'portuguese': 'pt', 'portugal': 'pt', 'lisbon': 'pt',
    'dutch': 'nl', 'netherlands': 'nl', 'holland': 'nl', 'amsterdam': 'nl', 'rotterdam': 'nl',
    'belgian': 'be', 'belgium': 'be', 'brussels': 'be',
    'swedish': 'se', 'sweden': 'se', 'stockholm': 'se',
    'norwegian': 'no', 'norway': 'no', 'oslo': 'no',
    'danish': 'dk', 'denmark': 'dk', 'copenhagen': 'dk',
    'finnish': 'fi', 'finland': 'fi', 'helsinki': 'fi',
    'icelandic': 'is', 'iceland': 'is', 'reykjavik': 'is', 'reykjavík': 'is',
    'irish': 'ie', 'ireland': 'ie', 'dublin': 'ie', 'mullingar': 'ie',
    'polish': 'pl', 'poland': 'pl', 'warsaw': 'pl', 'poznań': 'pl', 'kraków': 'pl', 'krakow': 'pl', 'wrocław': 'pl', 'wroclaw': 'pl',
    'czech': 'cz', 'czech republic': 'cz', 'czechia': 'cz', 'prague': 'cz',
    'slovak': 'sk', 'slovakia': 'sk', 'bratislava': 'sk',
    'hungarian': 'hu', 'hungary': 'hu', 'budapest': 'hu',
    'romanian': 'ro', 'romania': 'ro', 'bucharest': 'ro',
    'bulgarian': 'bg', 'bulgaria': 'bg', 'sofia': 'bg',
    'serbian': 'rs', 'serbia': 'rs', 'belgrade': 'rs',
    'croatian': 'hr', 'croatia': 'hr', 'zagreb': 'hr',
    'slovenian': 'si', 'slovenia': 'si',
    'bosnian': 'ba', 'bosnia': 'ba',
    'greek': 'gr', 'greece': 'gr', 'athens': 'gr', 'thessaloniki': 'gr',
    'turkish': 'tr', 'turkey': 'tr', 'turkish-german': 'tr', 'istanbul': 'tr', 'ankara': 'tr',
    'russian': 'ru', 'russia': 'ru', 'moscow': 'ru',
    'ukrainian': 'ua', 'ukraine': 'ua', 'kyiv': 'ua', 'kiev': 'ua',
    'japanese': 'jp', 'japan': 'jp', 'tokyo': 'jp',
    'south korean': 'kr', 'korean': 'kr', 'south korea': 'kr', 'seoul': 'kr',
    'chinese': 'cn', 'china': 'cn', 'beijing': 'cn', 'shanghai': 'cn',
    'taiwanese': 'tw', 'taiwan': 'tw', 'taipei': 'tw',
    'indian': 'in', 'india': 'in', 'mumbai': 'in', 'delhi': 'in', 'bollywood': 'in',
    'thai': 'th', 'thailand': 'th', 'bangkok': 'th',
    'vietnamese': 'vn', 'vietnam': 'vn', 'hanoi': 'vn', 'ho chi minh': 'vn',
    'filipino': 'ph', 'philippines': 'ph', 'philippine': 'ph', 'manila': 'ph',
    'indonesian': 'id', 'indonesia': 'id', 'jakarta': 'id',
    'malaysian': 'my', 'malaysia': 'my', 'kuala lumpur': 'my',
    'singaporean': 'sg', 'singapore': 'sg',
    'mexican': 'mx', 'mexico': 'mx', 'mexico city': 'mx',
    'colombian': 'co', 'colombia': 'co', 'medellín': 'co', 'medellin': 'co', 'bogotá': 'co', 'bogota': 'co',
    'brazilian': 'br', 'brazil': 'br', 'são paulo': 'br', 'rio de janeiro': 'br',
    'argentine': 'ar', 'argentinian': 'ar', 'argentina': 'ar', 'buenos aires': 'ar',
    'chilean': 'cl', 'chile': 'cl', 'santiago': 'cl',
    'peruvian': 'pe', 'peru': 'pe', 'lima': 'pe',
    'venezuelan': 've', 'venezuela': 've', 'caracas': 've',
    'cuban': 'cu', 'cuba': 'cu',
    'dominican': 'do', 'dominican republic': 'do', 'santo domingo': 'do',
    'puerto rican': 'pr', 'puerto rico': 'pr',
    'panamanian': 'pa', 'panama': 'pa',
    'paraguayan': 'py', 'paraguay': 'py',
    'ecuadorian': 'ec', 'ecuador': 'ec',
    'south african': 'za', 'south africa': 'za', 'johannesburg': 'za', 'cape town': 'za', 'soweto': 'za',
    'nigerian': 'ng', 'nigeria': 'ng', 'lagos': 'ng',
    'kenyan': 'ke', 'kenya': 'ke',
    'egyptian': 'eg', 'egypt': 'eg', 'cairo': 'eg',
    'moroccan': 'ma', 'morocco': 'ma', 'casablanca': 'ma', 'rabat': 'ma',
    'algerian': 'dz', 'algeria': 'dz',
    'tunisian': 'tn', 'tunisia': 'tn',
    'saudi': 'sa', 'saudi arabian': 'sa', 'saudi arabia': 'sa',
    'emirati': 'ae', 'uae': 'ae', 'united arab emirates': 'ae', 'dubai': 'ae',
    'lebanese': 'lb', 'lebanon': 'lb', 'beirut': 'lb',
    'israeli': 'il', 'israel': 'il', 'tel aviv': 'il',
    'new zealand': 'nz', 'new zealander': 'nz', 'kiwi': 'nz',
    'lithuanian': 'lt', 'lithuania': 'lt', 'vilnius': 'lt',
    'latvian': 'lv', 'latvia': 'lv',
    'estonian': 'ee', 'estonia': 'ee',
    'albanian': 'al', 'albania': 'al', 'kosovar': 'xk', 'kosovo': 'xk',
    'montenegrin': 'me', 'montenegro': 'me',
    'north macedonian': 'mk', 'north macedonia': 'mk',
    'austrian': 'at', 'austria': 'at', 'vienna': 'at',
    'swiss': 'ch', 'switzerland': 'ch', 'zurich': 'ch',
    'luxembourgish': 'lu', 'luxembourg': 'lu',
    'congolese': 'cd', 'congo': 'cd',
    'ghanaian': 'gh', 'ghana': 'gh',
    'iraqi': 'iq', 'iraq': 'iq',
    'iranian': 'ir', 'iran': 'ir', 'persian': 'ir',
    'pakistani': 'pk', 'pakistan': 'pk',
    'jamaican': 'jm', 'jamaica': 'jm',
    'trinidadian': 'tt', 'trinidad': 'tt',
    'costa rican': 'cr', 'costa rica': 'cr',
    'honduran': 'hn', 'honduras': 'hn',
    'guatemalan': 'gt', 'guatemala': 'gt',
    'uruguayan': 'uy', 'uruguay': 'uy',
    'bolivian': 'bo', 'bolivia': 'bo',
}

# City to country mapping for common cities
CITY_COUNTRY = {
    'london': 'gb', 'manchester': 'gb', 'birmingham': 'gb', 'bristol': 'gb', 'liverpool': 'gb', 'leeds': 'gb', 'sheffield': 'gb', 'nottingham': 'gb', 'glasgow': 'gb', 'edinburgh': 'gb',
    'new york': 'us', 'los angeles': 'us', 'chicago': 'us', 'houston': 'us', 'atlanta': 'us', 'miami': 'us', 'detroit': 'us', 'philadelphia': 'us', 'dallas': 'us', 'san francisco': 'us', 'seattle': 'us', 'boston': 'us', 'new jersey': 'us', 'brooklyn': 'us', 'compton': 'us', 'harlem': 'us', 'queens': 'us', 'bronx': 'us', 'oakland': 'us', 'memphis': 'us', 'new orleans': 'us', 'nashville': 'us', 'denver': 'us', 'portland': 'us', 'pittsburgh': 'us', 'cleveland': 'us', 'baltimore': 'us', 'washington': 'us', 'st. louis': 'us', 'las vegas': 'us', 'san diego': 'us', 'phoenix': 'us', 'austin': 'us', 'minneapolis': 'us', 'indianapolis': 'us', 'charlotte': 'us', 'sacramento': 'us', 'milwaukee': 'us', 'kansas city': 'us', 'virginia': 'us', 'maryland': 'us', 'florida': 'us', 'california': 'us', 'texas': 'us', 'georgia': 'us', 'illinois': 'us', 'ohio': 'us', 'michigan': 'us', 'pennsylvania': 'us', 'north carolina': 'us', 'new york city': 'us', 'la': 'us',
    'paris': 'fr', 'marseille': 'fr', 'lyon': 'fr', 'toulouse': 'fr', 'nice': 'fr', 'nantes': 'fr', 'strasbourg': 'fr', 'bordeaux': 'fr', 'lille': 'fr',
    'berlin': 'de', 'hamburg': 'de', 'munich': 'de', 'cologne': 'de', 'frankfurt': 'de', 'düsseldorf': 'de', 'stuttgart': 'de',
    'rome': 'it', 'milan': 'it', 'naples': 'it', 'turin': 'it', 'florence': 'it', 'genoa': 'it', 'bologna': 'it', 'palermo': 'it',
    'madrid': 'es', 'barcelona': 'es', 'seville': 'es', 'valencia': 'es', 'málaga': 'es', 'bilbao': 'es',
    'lisbon': 'pt', 'porto': 'pt',
    'amsterdam': 'nl', 'rotterdam': 'nl', 'the hague': 'nl', 'utrecht': 'nl', 'eindhoven': 'nl', 'surinamese-dutch': 'nl',
    'brussels': 'be', 'antwerp': 'be',
    'stockholm': 'se', 'gothenburg': 'se', 'malmö': 'se',
    'oslo': 'no', 'bergen': 'no', 'trondheim': 'no',
    'copenhagen': 'dk', 'aarhus': 'dk',
    'helsinki': 'fi', 'espoo': 'fi', 'tampere': 'fi',
    'dublin': 'ie', 'cork': 'ie', 'mullingar': 'ie',
    'warsaw': 'pl', 'kraków': 'pl', 'krakow': 'pl', 'wrocław': 'pl', 'gdańsk': 'pl', 'poznań': 'pl', 'łódź': 'pl', 'katowice': 'pl',
    'prague': 'cz', 'brno': 'cz',
    'bratislava': 'sk', 'košice': 'sk',
    'budapest': 'hu',
    'bucharest': 'ro', 'cluj': 'ro',
    'sofia': 'bg', 'plovdiv': 'bg',
    'belgrade': 'rs', 'novi sad': 'rs',
    'zagreb': 'hr',
    'athens': 'gr', 'thessaloniki': 'gr',
    'istanbul': 'tr', 'ankara': 'tr', 'izmir': 'tr',
    'moscow': 'ru', 'saint petersburg': 'ru', 'st. petersburg': 'ru',
    'kyiv': 'ua', 'kiev': 'ua', 'kharkiv': 'ua', 'odesa': 'ua', 'odessa': 'ua',
    'tokyo': 'jp', 'osaka': 'jp', 'yokohama': 'jp',
    'seoul': 'kr', 'busan': 'kr', 'incheon': 'kr',
    'beijing': 'cn', 'shanghai': 'cn', 'guangzhou': 'cn', 'shenzhen': 'cn', 'hong kong': 'hk',
    'taipei': 'tw', 'kaohsiung': 'tw',
    'mumbai': 'in', 'delhi': 'in', 'bangalore': 'in', 'hyderabad': 'in', 'chennai': 'in', 'kolkata': 'in', 'pune': 'in',
    'bangkok': 'th', 'chiang mai': 'th',
    'hanoi': 'vn', 'ho chi minh city': 'vn', 'saigon': 'vn',
    'manila': 'ph', 'cebu': 'ph', 'quezon city': 'ph',
    'jakarta': 'id', 'surabaya': 'id', 'bandung': 'id',
    'kuala lumpur': 'my',
    'singapore': 'sg',
    'mexico city': 'mx', 'guadalajara': 'mx', 'monterrey': 'mx',
    'bogotá': 'co', 'bogota': 'co', 'medellín': 'co', 'medellin': 'co', 'cali': 'co',
    'são paulo': 'br', 'rio de janeiro': 'br', 'brasília': 'br',
    'buenos aires': 'ar',
    'santiago': 'cl',
    'lima': 'pe',
    'caracas': 've', 'maracaibo': 've',
    'havana': 'cu',
    'santo domingo': 'do',
    'san juan': 'pr',
    'panama city': 'pa',
    'asunción': 'py', 'asuncion': 'py',
    'johannesburg': 'za', 'cape town': 'za', 'durban': 'za', 'pretoria': 'za', 'soweto': 'za',
    'lagos': 'ng', 'abuja': 'ng',
    'nairobi': 'ke',
    'cairo': 'eg', 'alexandria': 'eg',
    'casablanca': 'ma', 'rabat': 'ma', 'marrakech': 'ma', 'fez': 'ma',
    'algiers': 'dz',
    'tunis': 'tn',
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
    'zurich': 'ch', 'geneva': 'ch', 'bern': 'ch',
    'accra': 'gh',
    'kingston': 'jm',
    'toronto': 'ca', 'montreal': 'ca', 'vancouver': 'ca', 'ottawa': 'ca', 'calgary': 'ca',
    'sydney': 'au', 'melbourne': 'au', 'brisbane': 'au', 'perth': 'au',
    'vallenato': 'co',
}


def extract_nationality(text, artist_name):
    """Extract nationality/country from Wikipedia extract text."""
    if not text:
        return None, None
    
    text_lower = text.lower()
    
    # Pattern 1: "is a/an [nationality] [profession]"
    patterns = [
        r'is (?:a|an) ([A-Za-z\-\s]+?)(?:\s+(?:singer|rapper|musician|band|group|artist|songwriter|producer|DJ|dj|composer|vocalist|actor|actress|entertainer|record producer|hip hop|pop|rock|electronic|R&B|soul|folk|country|classical|jazz|reggae|dancehall|afrobeat|amapiano))',
        r'is (?:a|an) ([A-Za-z\-\s]+?)(?:\s+(?:musical|music|recording|hip-hop|indie|alternative|dance|punk|metal|rap|trap|drill|grime|k-pop|j-pop))',
        r'(?:born|raised|from|based) in ([A-Za-z\s\-\.\,]+?)(?:\.|,|\))',
        r'from ([A-Za-z\s\-]+?), ([A-Za-z\s]+?)(?:\.|,|\)| is)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    # Check city, state/country format
                    for part in match:
                        part_clean = part.strip().lower()
                        if part_clean in NATIONALITY_MAP:
                            return NATIONALITY_MAP[part_clean], f"matched '{part.strip()}'"
                        if part_clean in CITY_COUNTRY:
                            return CITY_COUNTRY[part_clean], f"city match '{part.strip()}'"
                else:
                    match_clean = match.strip().lower()
                    # Check if it's a known nationality
                    if match_clean in NATIONALITY_MAP:
                        return NATIONALITY_MAP[match_clean], f"matched '{match.strip()}'"
                    # Check individual words
                    for word in match_clean.split():
                        if word in NATIONALITY_MAP:
                            return NATIONALITY_MAP[word], f"word match '{word}'"
                        if word in CITY_COUNTRY:
                            return CITY_COUNTRY[word], f"city word '{word}'"
    
    # Pattern: check for nationality words anywhere in first 2 sentences
    first_sentences = '. '.join(text.split('.')[:3]).lower()
    
    # Check for explicit nationalities first (longer matches first)
    sorted_nationalities = sorted(NATIONALITY_MAP.keys(), key=len, reverse=True)
    for nat in sorted_nationalities:
        if len(nat) < 4:  # Skip very short matches to avoid false positives
            continue
        if nat in first_sentences:
            # Make sure it's not part of a longer word
            idx = first_sentences.find(nat)
            before = first_sentences[idx-1] if idx > 0 else ' '
            after = first_sentences[idx+len(nat)] if idx+len(nat) < len(first_sentences) else ' '
            if not before.isalpha() and not after.isalpha():
                return NATIONALITY_MAP[nat], f"found '{nat}' in intro"
    
    # Check cities in first sentences
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


def query_wikipedia(artist_name):
    """Query Wikipedia API for artist info."""
    # First try direct title lookup
    encoded_name = urllib.parse.quote(artist_name)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded_name}&prop=extracts&exintro=true&format=json&explaintext=true"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'VizConValidation/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                if page_id != '-1' and 'extract' in page:
                    return page['extract'], page.get('title', '')
    except Exception as e:
        pass
    
    # If direct lookup fails, try search API
    search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded_name}&limit=3&format=json"
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'VizConValidation/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if len(data) > 1 and data[1]:
                # Try first result
                for title in data[1][:3]:
                    encoded_title = urllib.parse.quote(title)
                    detail_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded_title}&prop=extracts&exintro=true&format=json&explaintext=true"
                    req2 = urllib.request.Request(detail_url, headers={'User-Agent': 'VizConValidation/1.0'})
                    with urllib.request.urlopen(req2, timeout=10) as resp2:
                        detail = json.loads(resp2.read().decode())
                        pages = detail.get('query', {}).get('pages', {})
                        for page_id, page in pages.items():
                            if page_id != '-1' and 'extract' in page:
                                extract = page['extract']
                                # Check if it's music-related
                                music_keywords = ['singer', 'rapper', 'musician', 'band', 'group', 'artist', 'songwriter', 'producer', 'DJ', 'album', 'single', 'song', 'music', 'hip hop', 'pop', 'rock', 'record']
                                if any(kw in extract.lower() for kw in music_keywords):
                                    return extract, title
                    time.sleep(0.2)
    except Exception as e:
        pass
    
    return None, None


def query_wikipedia_with_suffix(artist_name):
    """Try Wikipedia with common music suffixes."""
    suffixes = ['', ' (singer)', ' (rapper)', ' (musician)', ' (band)', ' (DJ)', ' (music group)', ' (Filipino singer)', ' (artist)']
    
    for suffix in suffixes:
        name_to_try = artist_name + suffix
        extract, title = query_wikipedia(name_to_try)
        if extract:
            # Verify it's about music
            music_keywords = ['singer', 'rapper', 'musician', 'band', 'group', 'artist', 'songwriter', 'producer', 'dj', 'album', 'single', 'song', 'music', 'hip hop', 'pop', 'rock', 'record', 'vocal', 'genre', 'label', 'track']
            extract_lower = extract.lower()
            if any(kw in extract_lower for kw in music_keywords):
                return extract, title
            elif suffix == '':
                # For direct match, accept it even if not clearly music
                # but store it and keep looking
                first_result = (extract, title)
                continue
        time.sleep(0.3)
    
    # If we found something on direct match but nothing music-specific with suffixes
    if 'first_result' in dir():
        return first_result
    
    return None, None


def main():
    input_path = '/Users/gabmc/Library/CloudStorage/OneDrive-amazon.com/4. Claude/vizcon-project/data/validation_sample_100.json'
    output_path = '/Users/gabmc/Library/CloudStorage/OneDrive-amazon.com/4. Claude/vizcon-project/data/validation_results_100.json'
    
    with open(input_path, 'r', encoding='utf-8') as f:
        artists = json.load(f)
    
    results = []
    total = len(artists)
    
    for i, artist in enumerate(artists):
        full_name = artist['name']
        our_country = artist['our_country']
        
        # Use only first name before pipe
        lookup_name = full_name.split('|')[0].strip()
        
        print(f"[{i+1}/{total}] Looking up: {lookup_name}", flush=True)
        
        extract, wiki_title = query_wikipedia_with_suffix(lookup_name)
        
        if extract:
            country_code, note = extract_nationality(extract, lookup_name)
            if country_code:
                match = (country_code == our_country)
                results.append({
                    'name': full_name,
                    'our_country': our_country,
                    'wiki_country': country_code,
                    'match': match,
                    'wiki_note': f"{note} (wiki: {wiki_title})"
                })
                status = "MATCH" if match else f"MISMATCH (ours={our_country}, wiki={country_code})"
                print(f"  -> {status}: {note}", flush=True)
            else:
                results.append({
                    'name': full_name,
                    'our_country': our_country,
                    'wiki_country': 'unknown',
                    'match': None,
                    'wiki_note': f"Wikipedia page found ({wiki_title}) but no nationality extracted"
                })
                print(f"  -> No nationality found in extract", flush=True)
        else:
            results.append({
                'name': full_name,
                'our_country': our_country,
                'wiki_country': 'unknown',
                'match': None,
                'wiki_note': 'No Wikipedia page found'
            })
            print(f"  -> No Wikipedia page found", flush=True)
        
        # Rate limiting
        time.sleep(0.5)
    
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
            print(f"  {r['name']}: ours={r['our_country']}, wiki={r['wiki_country']} ({r['wiki_note']})")
    
    if not_found:
        print(f"\nNOT FOUND / NO NATIONALITY ({len(not_found)}):")
        print("-"*60)
        for r in not_found:
            print(f"  {r['name']} (assigned: {r['our_country']})")


if __name__ == '__main__':
    main()

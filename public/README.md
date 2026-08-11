# If music were the only currency, how rich would your country be?

**VizContest 2026** — Amazon Analyticon
**Theme:** How the world lives, thrives, and connects
**Author:** gabmc@amazon.co.jp

## Live Visualization

https://vizcon-2026.vercel.app

## Story

We treat Spotify's daily top-200 charts across 100 countries (42.8 million rows, 2017–2025) as an international trade economy. When a song charts outside its home country, that is an export. Nine years of streaming data, read as a balance of payments — revealing which countries set trends, which spread them, and how the world is quietly going local.

## Data Sources

All data is publicly accessible and downloadable:

| Source | Description | Link |
|--------|-------------|------|
| Spotify Charts Daily (Updated) | Daily top-200 charts for 70+ countries, 2017–2025. 42.8M rows. Primary dataset. | [Kaggle: gonzalopezgil/spotify-charts-daily-updated](https://www.kaggle.com/datasets/gonzalopezgil/spotify-charts-daily-updated) |
| Wikipedia | Artist nationality identification (primary source) | [wikipedia.org](https://www.wikipedia.org/) |
| Wikidata | Structured artist nationality data via SPARQL queries | [wikidata.org](https://www.wikidata.org/) |
| MusicBrainz | Open music encyclopedia for artist origin verification | [musicbrainz.org](https://musicbrainz.org/) |
| Top 10K Musical Talents: America's Chart-Toppers | Supplementary artist-country mapping (Kaggle) | [Kaggle: daniyalalikhan/top-10k-musical-talents-americas-chart-toppers](https://www.kaggle.com/datasets/daniyalalikhan/top-10k-musical-talents-americas-chart-toppers) |

### Artist Nationality Mapping

84,985 unique artists were mapped to 1–2 home countries using the sources above plus LLM-assisted research (Claude, Anthropic). Coverage: 99.9%. Dual-nationality artists count as local in both countries, with export credit split equally.

## Methodology

- **Period:** 2017–2025 (nine complete years). 2016 excluded — only 4,706 chart-weeks vs 270,171 in 2017.
- **Reach (chart-weeks):** One song, on one country's top 100, for one week. Every market counts equally.
- **Currency (streams):** Population-weighted by construction; larger markets contribute more.
- **Export:** A chart-week earned by an artist outside their country of origin.
- **Trade surplus:** A country's artists earned more chart-weeks abroad than foreign artists earned on its home chart.
- **Grouping:** Ward hierarchical clustering on 13 standardised metrics, Euclidean distance (cophenetic correlation 0.96). The United States is held out as an outlier.
- **Limitations:** Chart start dates vary by country (56 in 2017, 70 by 2022). Artist-origin assignment is imperfect for relocated/dual-nationality artists. Puerto Rico and Hong Kong are territories. Streaming skews younger and urban.

## Tools Used

- **Visualization:** D3.js v7, static HTML, CSS
- **Data Pipeline:** Python 3, pandas
- **Hosting:** Vercel (auto-deploy from GitHub)
- **Analysis:** Excel (9-sheet workbook)

## GenAI Usage

Claude (Anthropic) was used for:

1. **Data pipeline code** — Python scripts for aggregating 10.5 GB of daily CSVs into weekly top-100 per country
2. **Artist nationality mapping** — LLM-assisted classification for artists not found in Wikipedia/Wikidata/MusicBrainz
3. **Statistical analysis** — Clustering methodology, metric standardization, significance testing
4. **Narrative drafting** — Story arc development and copy editing
5. **Visualization code** — D3.js chart implementations, scroll interactions, responsive layouts

All findings were verified against source data. The author directed every analytical and narrative choice.

## Repository Structure

```
public/
├── index.html              # Main visualization (all data inlined)
├── music_economy.json      # Per-country metrics, time series, rankings
├── country_profiles.json   # 100 countries with 17 lenses + top100 songs/artists
├── country_pairs.json      # Bilateral flows between all country pairs
├── artist_concentration.json  # Top-N artist share per country
└── yearly_champions.json   # Yearly top song + top artist (2017–2025)
data/
├── artist_countries_final.json  # Final artist-to-country mapping (84,985 artists)
└── validate_countries.py        # Validation scripts for artist nationality accuracy
```

## License

Data sourced under respective dataset licenses (CC0-1.0, CC BY, open access). Visualization code is original work.

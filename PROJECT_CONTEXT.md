# VizContest 2026: What if music were a global currency?

## Project Summary

**Competition:** Amazon Analyticon VizContest 2026
**Theme:** "How the world lives, thrives, and connects"
**Angle:** We treat Spotify's daily top-200 charts across 100 countries (42.8M rows, 2017-2025) as an international trade economy. When a song charts outside its home country, that is an export.
**Key message:** How music connects the world.
**Deadline:** August 10, 2026
**Live URL:** is-my-country-rich-in-music-currency-vizcon-2026.vercel.app
**Repo:** GitHub `Christianetti/vizcon-2026`

---


## Pages

### `index.html` (1,134 lines) - Full-Screen Slides (CHOSEN)

The winning variant. Full-viewport snap-scroll slides (100svh). Split layout: text left (40%), viz right (60%). Navigation dots on the right edge. Bold color-tinted backgrounds per section. 11 Spotify embeds for interactivity. Joy voice throughout.


**Layout:** `scroll-snap-type: y mandatory` with `grid-template-columns: 2fr 3fr`. On mobile (< 768px): stacks vertically. Each section is one screen.

**Sections (9 slides):**
1. **Hero** -

H1 Element "What if music was the only currency for world's countries economies?"

H2 Element "How connected would be yours?"
Description "A brief Spotify Top-100 weekly charts from 70 countries since 2017."

Visuals: I would like to have a world map in the background where only the 70 mapped countries appears and their size grows and reduces randomly in a floated way like bubbles.

Sound: a random top 100 songs with Spotify player. A tiny description below the Spotify Widget: [Song Name, Artist Name] - #(position number) Top Ranking from 2017 - 2026.


---

## Data Files (JSON, in `public/`)

| File | Size | Content |
|------|------|---------|
| `music_economy.json` | 431 KB | Per-country summary metrics + time_series + rankings |
| `country_profiles.json` | 128 KB | 100 countries with 17 lenses + top100 songs/artists + language groups |
| `country_pairs.json` | 478 KB | Bilateral flows between all country pairs |
| `artist_concentration.json` | 5 KB | Top-N artist share per country |
| `yearly_champions.json` | ~3 KB | Yearly top song + top artist (2017-2025) |

---

## Design System

- **Fonts:** DM Sans (headings, UI), Lora (body, editorial)
- **Background:** #e6e5e5ff (white gray)
- **Palette:** Mostly black, gray and white. But highlights in  #3a7fa7ff 
- **Mobile reference:** iPhone 15 (393x852)
- **Voice:** Joy (Inside Out) - celebratory, "we" language, connection-focused.

---

## Tech Stack

- Static HTML (no build step, no framework)
- D3.js v7 (charts, data binding)
- Spotify embed iframes (30-second previews, no API key needed)
- IntersectionObserver (scroll animations, nav dot tracking)
- Vercel (auto-deploys from GitHub `public/` folder)
- Data pipeline: Python 3 (pandas)

---

## What We Built

### Data Pipeline (Python)

Located in `src/pipeline/`. Evolved through 5 iterations:

| Script | Purpose |
|--------|---------|
| `build_weekly_dataset.py` | Raw 10.5 GB daily CSV to weekly top-100 per country (309 MB) |
| `build_music_economy_v5.py` | Weekly data to JSON (all 17 analytical lenses per country) |
| `build_data.py` | Supplementary data builds |

**Artist nationality mapping:** 84,985 artists mapped to 1-2 home countries using Wikipedia, Wikidata, MusicBrainz, Kaggle, and LLM-assisted research. 99.9% coverage.

### Analysis (Excel)

`music_trade_economy_analysis.xlsx` - 9 sheets covering export rankings, concentration, longevity, spread, collaboration rates, cultural blocs, and time-series trends.

### Narrative Script

`narrative_script.md` - Full narrative arc (originally owl-voiced, later replaced by Joy voice in the HTML).

### Visualization (Static HTML + D3.js)

Deployed on Vercel from `public/` folder. All pages use D3.js v7 and load pre-aggregated JSON data.

---

## Status

| Phase | Status |
|-------|--------|
| Data pipeline (5 iterations) | Done |
| Artist nationality mapping (99.9%) | Done |
| 17 analytical lenses | Done |
| Excel analysis workbook | Done |
| Narrative script | Done |
| V1 - Continuous scroll | Done (not chosen) |
| V2 - Card story | Done (not chosen) |
| V3 - Full-screen slides | Done (chosen) |
| Narrative refinement (Joy voice) | Done |
| Deploy V3 as index.html | Pending |
| Final Vercel deployment | Pending |
| VizCon submission | Pending |

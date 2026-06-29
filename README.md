# Short-Form Video Ad Market Analysis

Competitive analysis of the short-form video advertising landscape — **TikTok**,
**Instagram Reels**, and **YouTube Shorts** — comparing monetization models and
ad-load strategies to identify where each platform captures advertiser spend and
where ad budgets are likely to shift.

## What it does
- Builds a transparent dataset of platform ad revenue, reach, ad load, and ad
  ARPU from publicly reported 2023–2025 estimates.
- Computes competitive metrics: revenue share, ad ARPU, and a **monetization
  efficiency** ratio (ARPU per point of ad load).
- Estimates **ad-load headroom** per platform.
- Projects a 5-year ad-revenue path and produces a recommendation on where
  advertiser spend is likely to move.

## Quickstart
```bash
pip install -r requirements.txt
python data/generate_data.py      # writes data/platforms.csv, data/projections.csv
python src/analysis.py            # prints metrics, saves figures to outputs/
```
Or open `notebooks/short_form_video_ad_analysis.ipynb` for the narrative walk-through.

## Structure
```
data/generate_data.py   # assumptions + dataset generation (edit to run scenarios)
src/analysis.py         # metrics, projection, figures
notebooks/              # narrative analysis notebook
outputs/                # generated figures + metrics CSV
```

## Data disclaimer
Figures are seeded from public estimates (earnings calls, eMarketer / Insider
Intelligence, press reporting) and are a reproducible approximation, **not**
audited financials. Edit the `ASSUMPTIONS` block in `data/generate_data.py` to
run your own scenarios.

## Author
Harry Vo — https://github.com/harry-vo-uma

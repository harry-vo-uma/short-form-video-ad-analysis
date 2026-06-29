"""
Generate the dataset for the short-form video ad market analysis.

Figures are seeded from publicly reported 2023-2025 estimates (company
earnings calls, eMarketer / Insider Intelligence, press reporting) and are
intended as a transparent, reproducible approximation rather than audited
financials. Adjust ASSUMPTIONS below to run your own scenarios.
"""
from __future__ import annotations
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# ASSUMPTIONS (publicly reported / estimated; edit to run scenarios)
# ---------------------------------------------------------------------------
# Global ad revenue ($B) attributable to short-form video surfaces.
PLATFORMS = {
    "TikTok":       {"owner": "ByteDance", "ad_rev_2024_b": 23.6, "mau_m": 1100,
                     "ad_load_pct": 9.0, "monetization": "in-feed + Spark + Shop"},
    "Instagram Reels": {"owner": "Meta",   "ad_rev_2024_b": 22.0, "mau_m": 2000,
                     "ad_load_pct": 6.5, "monetization": "in-feed (Meta Ads)"},
    "YouTube Shorts":  {"owner": "Alphabet","ad_rev_2024_b": 8.5, "mau_m": 2000,
                     "ad_load_pct": 4.0, "monetization": "in-feed (skippable) + share"},
}

# Rough year-over-year ad-revenue growth rates by platform (estimated).
GROWTH = {
    "TikTok":          [0.42, 0.38, 0.28, 0.22, 0.18],
    "Instagram Reels": [0.35, 0.30, 0.24, 0.20, 0.16],
    "YouTube Shorts":  [0.60, 0.50, 0.40, 0.32, 0.26],
}
START_YEAR = 2024


def platform_table() -> pd.DataFrame:
    rows = []
    for name, p in PLATFORMS.items():
        arpu = p["ad_rev_2024_b"] * 1e9 / (p["mau_m"] * 1e6)  # ad $ per MAU / yr
        rows.append({
            "platform": name,
            "owner": p["owner"],
            "ad_rev_2024_b": p["ad_rev_2024_b"],
            "mau_m": p["mau_m"],
            "ad_load_pct": p["ad_load_pct"],
            "ad_arpu_usd": round(arpu, 2),
            "monetization": p["monetization"],
        })
    return pd.DataFrame(rows)


def projection_table() -> pd.DataFrame:
    rows = []
    for name, p in PLATFORMS.items():
        rev = p["ad_rev_2024_b"]
        for i, g in enumerate(GROWTH[name]):
            year = START_YEAR + i
            rows.append({"platform": name, "year": year,
                         "ad_rev_b": round(rev, 2), "yoy_growth": g})
            rev = rev * (1 + g)
    return pd.DataFrame(rows)


def main() -> None:
    platform_table().to_csv("data/platforms.csv", index=False)
    projection_table().to_csv("data/projections.csv", index=False)
    print("Wrote data/platforms.csv and data/projections.csv")


if __name__ == "__main__":
    main()

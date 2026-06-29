"""
Short-form video ad market analysis.

Loads the generated tables, computes competitive metrics (revenue share,
ad ARPU, monetization efficiency), projects a 5-year ad-revenue path, and
saves figures to outputs/. Run `python data/generate_data.py` first.
"""
from __future__ import annotations
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless-safe
import matplotlib.pyplot as plt

OUT = "outputs"


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    plats = pd.read_csv("data/platforms.csv")
    proj = pd.read_csv("data/projections.csv")
    return plats, proj


def competitive_metrics(plats: pd.DataFrame) -> pd.DataFrame:
    df = plats.copy()
    total = df["ad_rev_2024_b"].sum()
    df["rev_share_pct"] = (df["ad_rev_2024_b"] / total * 100).round(1)
    # Monetization efficiency: ad ARPU normalized by ad load.
    # Higher = more $ per user per unit of ad load (room to scale ad load).
    df["monetization_efficiency"] = (df["ad_arpu_usd"] / df["ad_load_pct"]).round(2)
    return df.sort_values("rev_share_pct", ascending=False)


def headroom(plats: pd.DataFrame) -> pd.DataFrame:
    """Estimate ad-load headroom vs the highest-load platform."""
    df = plats.copy()
    ceiling = df["ad_load_pct"].max()
    df["ad_load_headroom_pct"] = (ceiling - df["ad_load_pct"]).round(1)
    return df[["platform", "ad_load_pct", "ad_load_headroom_pct"]]


def plot_rev_share(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df["platform"], df["ad_rev_2024_b"])
    for i, v in enumerate(df["ad_rev_2024_b"]):
        ax.text(i, v + 0.3, f"${v}B", ha="center", fontsize=9)
    ax.set_title("Estimated 2024 short-form video ad revenue")
    ax.set_ylabel("Ad revenue ($B)")
    fig.tight_layout()
    path = os.path.join(OUT, "fig_revenue_2024.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def plot_projection(proj: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, g in proj.groupby("platform"):
        ax.plot(g["year"], g["ad_rev_b"], marker="o", label=name)
    ax.set_title("Projected short-form ad revenue (2024-2028)")
    ax.set_ylabel("Ad revenue ($B)")
    ax.set_xlabel("Year")
    ax.legend()
    fig.tight_layout()
    path = os.path.join(OUT, "fig_projection.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    plats, proj = load()
    metrics = competitive_metrics(plats)
    head = headroom(plats)

    print("\n=== Competitive metrics (2024) ===")
    print(metrics[["platform", "ad_rev_2024_b", "rev_share_pct",
                   "ad_arpu_usd", "ad_load_pct", "monetization_efficiency"]]
          .to_string(index=False))

    print("\n=== Ad-load headroom ===")
    print(head.to_string(index=False))

    # 2028 endpoint per platform.
    end = (proj.sort_values("year").groupby("platform").tail(1)
           [["platform", "year", "ad_rev_b"]])
    print("\n=== Projected 2028 ad revenue ===")
    print(end.to_string(index=False))

    f1 = plot_rev_share(metrics)
    f2 = plot_projection(proj)
    metrics.to_csv(os.path.join(OUT, "competitive_metrics.csv"), index=False)
    print(f"\nSaved {f1}, {f2}, and outputs/competitive_metrics.csv")

    # Headline takeaway.
    leader = metrics.iloc[0]["platform"]
    most_eff = metrics.sort_values("monetization_efficiency", ascending=False).iloc[0]
    print("\n=== Takeaway ===")
    print(f"- {leader} leads 2024 ad revenue share at "
          f"{metrics.iloc[0]['rev_share_pct']}%.")
    print(f"- {most_eff['platform']} shows the highest monetization efficiency "
          f"({most_eff['monetization_efficiency']}), implying room to raise ad "
          f"load and capture incremental advertiser spend.")


if __name__ == "__main__":
    main()

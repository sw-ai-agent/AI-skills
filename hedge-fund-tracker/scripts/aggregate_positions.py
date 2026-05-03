#!/usr/bin/env python3
"""
aggregate_positions.py — Cross-fund position aggregation.

Takes a JSON file (or stdin) describing each fund's top holdings and produces
two ranked tables:

  1. Equal-weighted (each fund counts as 1/N regardless of AUM)
  2. AUM-weighted   (dollar value = pct_of_portfolio * fund_aum_billions)

Equal-weighted is usually the more meaningful view because mega-funds like
Berkshire would otherwise dominate purely through size.

Always merges GOOG and GOOGL into a single 'GOOGL (Alphabet)' ticker.

Usage:
    python aggregate_positions.py funds.json
    cat funds.json | python aggregate_positions.py
    python aggregate_positions.py funds.json --top 20 --format json

Input JSON shape:
{
  "funds": [
    {
      "name": "Sanders Capital",
      "aum_b": 86.8,
      "holdings": [
        {"ticker": "GOOG",  "company": "Alphabet (C)", "pct": 11.53},
        {"ticker": "TSM",   "company": "TSMC",         "pct": 11.19},
        ...
      ]
    },
    ...
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


# Tickers that should be merged. Map any in the keys to the canonical ticker.
TICKER_ALIASES = {
    "GOOG":  "GOOGL",
    "GOOGL": "GOOGL",
}

CANONICAL_NAMES = {
    "GOOGL": "Alphabet (GOOG/GOOGL)",
}


def normalise_ticker(ticker: str) -> str:
    t = (ticker or "").strip().upper()
    return TICKER_ALIASES.get(t, t)


def aggregate(funds: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute equal-weighted and AUM-weighted aggregations."""
    n_funds = len(funds)
    if n_funds == 0:
        return {"equal_weighted": [], "aum_weighted": [], "n_funds": 0}

    sum_pct: dict[str, float] = defaultdict(float)
    sum_dollars: dict[str, float] = defaultdict(float)
    holders: dict[str, list[dict[str, Any]]] = defaultdict(list)
    name_for: dict[str, str] = {}

    for fund in funds:
        fund_name = fund["name"]
        aum_b = float(fund.get("aum_b", 0))

        # Track which tickers we've seen for this fund (for GOOG/GOOGL merge)
        # so we sum them rather than overwriting
        per_fund_pct: dict[str, float] = defaultdict(float)
        per_fund_company: dict[str, str] = {}

        for h in fund.get("holdings", []):
            t = normalise_ticker(h["ticker"])
            if not t:
                continue
            pct = float(h.get("pct", 0))
            per_fund_pct[t] += pct
            per_fund_company[t] = CANONICAL_NAMES.get(t, h.get("company", t))

        for ticker, pct in per_fund_pct.items():
            sum_pct[ticker] += pct
            sum_dollars[ticker] += pct / 100 * aum_b   # billions
            holders[ticker].append({
                "fund": fund_name,
                "pct": round(pct, 3),
                "dollars_b": round(pct / 100 * aum_b, 4),
            })
            name_for[ticker] = per_fund_company[ticker]

    def _build(metric_dict: dict[str, float], metric_label: str) -> list[dict]:
        rows = []
        for ticker, val in sorted(metric_dict.items(), key=lambda x: x[1], reverse=True):
            avg_pct = sum_pct[ticker] / n_funds
            rows.append({
                "ticker": ticker,
                "company": name_for[ticker],
                "n_funds_holding": len(holders[ticker]),
                "avg_pct_equal_wt": round(avg_pct, 3),
                "total_dollars_b": round(sum_dollars[ticker], 3),
                "holders": sorted(holders[ticker], key=lambda r: r["pct"], reverse=True),
            })
        return rows

    return {
        "n_funds": n_funds,
        "total_aum_b": round(sum(float(f.get("aum_b", 0)) for f in funds), 2),
        "equal_weighted": _build(sum_pct, "avg_pct"),
        "aum_weighted":   _build(sum_dollars, "dollars"),
    }


def render_text(result: dict[str, Any], top: int = 15) -> str:
    """Pretty-print the result for terminal viewing."""
    lines = []
    lines.append(f"\nN funds: {result['n_funds']}  |  Combined AUM: ${result['total_aum_b']}B\n")

    lines.append("=" * 80)
    lines.append("EQUAL-WEIGHTED (each fund = 1/N regardless of AUM)")
    lines.append("=" * 80)
    lines.append(f"{'#':<3} {'TICKER':<10} {'COMPANY':<28} {'AVG %':>8}  {'#FUNDS':>7}")
    lines.append("-" * 80)
    for i, row in enumerate(result["equal_weighted"][:top], 1):
        lines.append(
            f"{i:<3} {row['ticker']:<10} {row['company'][:28]:<28} "
            f"{row['avg_pct_equal_wt']:>7.2f}%  {row['n_funds_holding']:>7}"
        )

    lines.append("")
    lines.append("=" * 80)
    lines.append("AUM-WEIGHTED ($B exposure)")
    lines.append("=" * 80)
    lines.append(f"{'#':<3} {'TICKER':<10} {'COMPANY':<28} {'TOTAL $B':>10}  {'#FUNDS':>7}")
    lines.append("-" * 80)
    for i, row in enumerate(result["aum_weighted"][:top], 1):
        lines.append(
            f"{i:<3} {row['ticker']:<10} {row['company'][:28]:<28} "
            f"${row['total_dollars_b']:>8.2f}B  {row['n_funds_holding']:>7}"
        )

    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="Path to funds JSON file (or read from stdin)")
    ap.add_argument("--top", type=int, default=15, help="Number of rows to show (default 15)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    if args.input:
        data = json.loads(Path(args.input).read_text())
    else:
        data = json.loads(sys.stdin.read())

    funds = data["funds"] if "funds" in data else data
    result = aggregate(funds)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render_text(result, top=args.top))


if __name__ == "__main__":
    main()

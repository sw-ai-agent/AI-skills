---
name: hedge-fund-tracker
description: Screen and analyze top-performing hedge funds and portfolio managers using HedgeFollow.com 13F data. Use this skill whenever the user wants to find best-performing hedge funds, compare fund managers, screen by criteria like AUM/rating/concentration, look up specific funds (Berkshire, Pershing Square, Coatue, Sanders Capital, etc.), aggregate positions across multiple funds to find consensus picks, build watchlists from smart money, or track what professional investors are buying — even if they don't explicitly say "HedgeFollow" or "13F". Trigger on phrases like "top hedge funds", "best fund managers", "what is [fund] buying", "smart money picks", "hedge fund consensus", "fund manager performance", "13F holdings", "compare these hedge funds", or any portfolio-manager comparison task.
---

# Hedge Fund Tracker

A skill for screening top hedge funds, scraping their 13F holdings live from HedgeFollow.com, and producing **equal-weighted aggregated positions** to surface true consensus picks among institutional smart money.

## When to use this skill

Use whenever the user wants to:
- Screen hedge funds by criteria (AUM, HedgeFollow rating, top-N concentration, performance)
- Compare multiple portfolio managers side-by-side
- Find consensus picks across a set of funds (where smart money agrees)
- Look up a specific fund's top holdings, rating, and concentration
- Build a "smart money" watchlist of stocks held by multiple top managers

## Critical context the user must understand

Before producing analysis, make sure the user knows these caveats. State them briefly inline; don't lecture.

1. **HedgeFollow data is 13F-only** — long U.S. equity positions only. No shorts, bonds, options premiums, cash, or non-U.S. holdings. Filed quarterly with a 45-day lag.
2. **"AUM" on HedgeFollow ≠ true fund AUM** — it's the 13F long equity portion. Total firm AUM is usually larger (often 1.3–2x).
3. **HedgeFollow's "performance" is a simulation** — it's the 3-year return of the fund's top-20 disclosed long holdings, equal- or manager-weighted. It is NOT the actual net-of-fees fund return.
4. **Star rating is paywalled in the table view** but readable from individual fund pages via the `fundRat` element's CSS width (e.g. `width: 96%` = 4.8★ out of 5).
5. **Cloudflare blocks rapid scraping** — pace fund-page visits with delays of 4+ seconds between fund pages. After ~10 rapid visits the site issues a JavaScript challenge that blocks automation for several minutes.

## Workflow

The typical workflow has 5 stages. Skip stages the user has already done.

### Stage 1 — Capture screening criteria

Ask the user for:
- **AUM threshold** (e.g. ≥ $10B). Default to 13F AUM unless they specify total firm AUM.
- **Star rating threshold** (e.g. ≥ 4★). Optional but recommended.
- **Concentration rule** (e.g. top-3 holdings > 30%). Common conviction screen.
- **Performance window** (3yr from HedgeFollow, or 5yr from public sources).
- **Fund-type filter**: hedge funds only, or all institutional investors.

Surface the inherent tension: high-rated funds tend to be diversified (low top-3 %), while concentrated funds (>30% top-3) often score lower on HedgeFollow's metric. The user may need to relax a constraint.

### Stage 2 — Screen on HedgeFollow

Navigate to the right list page:
- `https://hedgefollow.com/top-hedge-funds.php` — sorted by performance/rating
- `https://hedgefollow.com/largest-hedge-funds.php` — sorted by AUM

Set filters via the JS dropdowns: `top` (20/50/100), `institution_type` (popular_hedge_funds / hedge_funds / all), `top_by` (weighted3YPerfTop20 / 3YPerfTop20 / hf_rating).

The screener table is JavaScript-rendered. Use `scripts/scrape_screener.js` to extract rows after a 4-second wait. Note: Fund Rating column on the screener page is paywalled and shows blank — ratings must be pulled from individual fund pages.

### Stage 3 — Pull individual fund details

For each candidate fund, navigate to `https://hedgefollow.com/funds/<Fund+Name>` and extract:
- **Star rating** from `document.getElementById('fundRat').style.width` (e.g. `"96%"` = 4.8★)
- **AUM, holdings count, performance** from the summary table (table[0])
- **Top holdings** with ticker, % of portfolio, $ value from the holdings table (table[1])

Use `scripts/scrape_fund_page.js` for the extraction. **Pace your visits** — wait 4–6 seconds between fund pages to avoid Cloudflare's bot challenge. If you see "Just a moment..." in the page title, stop and wait 60+ seconds before retrying.

If Cloudflare blocks you mid-session, do not keep retrying — fall back to verified public sources (annual letters, FinanceCharts.com, Morningstar) and inform the user.

### Stage 4 — Aggregate positions across funds

This is where the skill produces its most valuable output. The user typically wants to see which stocks have the strongest cross-fund consensus.

**Always offer two views:**

1. **AUM-weighted aggregation** — sums dollar value of each ticker across funds. This view is dominated by the largest funds (especially Berkshire Hathaway at ~$274B). Useful for total exposure but skewed.

2. **Equal-weighted aggregation** — gives each fund weight 1/N regardless of AUM. This reveals true consensus among managers. Calculation:
   ```
   avg_pct(ticker) = sum(fund_position_pct) / N_funds
   ```
   where funds not holding the ticker contribute 0.

**Always normalise GOOG and GOOGL into a single "Alphabet" ticker** — they're the same company.

Use `scripts/aggregate_positions.py` for the calculation. It handles GOOG/GOOGL merging, equal vs AUM weighting, and outputs ranked tables.

### Stage 5 — Present results

Build an HTML artifact (preferred) or markdown table showing:
- For each fund: AUM, star rating, top-3 % concentration, 3-yr & 5-yr return vs S&P 500, pass/fail badge for the user's criteria
- Aggregated positions: top 10–20 tickers ranked by equal-weighted average %, with fund-by-fund breakdown for the top 5–10
- Always show "# of funds holding" alongside dollar/percent values — breadth of conviction is as important as size

For the HTML, use the dark-themed style in `references/output_template.html`. For markdown, use the structure in `references/output_format.md`.

## S&P 500 benchmarks (refresh quarterly)

As of May 2026:
- 3-yr CAGR: ~21.6% (SPY total return)
- 5-yr CAGR: ~13.0%
- 10-yr CAGR: ~15.0%

If running this skill > 3 months from May 2026, do a quick web search for current SPY CAGR before stating these numbers.

## Common funds and their HedgeFollow URLs

For convenience, see `references/fund_directory.md` for a list of the ~30 most commonly requested funds with their exact HedgeFollow URL slugs.

## Files in this skill

- `scripts/scrape_screener.js` — Browser JS to extract the top-hedge-funds / largest-hedge-funds table
- `scripts/scrape_fund_page.js` — Browser JS to extract rating + top holdings from a single fund page
- `scripts/aggregate_positions.py` — Python script for equal-weighted and AUM-weighted aggregation
- `references/fund_directory.md` — Common fund names → HedgeFollow URL slugs
- `references/output_template.html` — Dark-themed HTML template for results
- `references/output_format.md` — Markdown format spec for results
- `references/known_caveats.md` — Detailed notes on data limitations and edge cases

# Known Caveats & Edge Cases

Things to remember when running this skill. Read this file when you encounter
unexpected data or want to write a more honest analysis.

## 13F filing limitations

13Fs are mandatory quarterly filings by U.S. institutional investment managers
with $100M+ AUM. They have these structural limits:

- **Long U.S. equities only.** No short positions, no bonds, no commodities,
  no currencies, no cash, no non-U.S.-listed equities (with some ADR exceptions).
- **45-day reporting lag.** Q4 2025 holdings (Dec 31) are filed by Feb 14, 2026.
  Anything you scrape from HedgeFollow today reflects the most recent quarter
  ending up to ~135 days ago.
- **Quarterly snapshots only.** A position shown could have been opened the
  day before the quarter ended or held all year.
- **Confidential treatment requests.** Some funds (e.g. Berkshire) sometimes
  request the SEC delay disclosure of new positions for competitive reasons.
  These positions show up later than the rest of the filing.
- **Shared positions.** Some "funds" are actually divisions of a larger firm
  (e.g. BlackRock subsidiaries). Aggregating BlackRock's 13Fs counts the same
  shares many times.

## HedgeFollow-specific quirks

- **"AUM" shown by HedgeFollow is 13F AUM**, i.e. the total long-equity
  market value disclosed in the latest 13F. Real firm AUM is usually larger:
  Pershing Square shows $15.5B 13F but discloses $18.3B total; Sanders
  Capital shows $86.8B 13F but $122B total firm AUM.
- **"Performance" is a simulation.** HedgeFollow takes the fund's top-20
  disclosed long positions and simulates how that sub-portfolio would have
  performed over the past 3 years. It is *not* the actual net-of-fees fund
  return that an investor in the fund would have earned. Two consequences:
  - Funds that hold lots of short positions or non-U.S. assets look better
    or worse than reality
  - High-turnover funds (Point72, Citadel) may have stale top-20 baskets
- **Star rating is paywalled in the screener tables** (the "Fund Rating"
  column comes back blank for all rows). To get a fund's rating you must
  navigate to its individual profile page and read the `fundRat` element's
  CSS width.
- **The site is JavaScript-rendered.** Static HTML scraping returns empty
  tables. You must use the browser tool with a 4+ second wait for tables
  to populate.
- **Cloudflare bot protection.** After ~10 rapid page navigations the site
  shows "Just a moment..." and blocks scraping for several minutes. Pace
  yourself: 4–6 seconds between fund pages. If blocked, wait 60+ seconds
  before retrying or fall back to public sources.

## Star rating decoding

The visible 5-star bar on each fund page is two stacked spans: an empty grey
background and an active orange overlay with `style="width:NN%"`. The width
percentage is rating-out-of-5:

| width | stars |
|-------|-------|
| 100% | 5.0 |
| 96%  | 4.8 |
| 80%  | 4.0 |
| 60%  | 3.0 |
| 40%  | 2.0 |

`stars = round(width_pct / 100 * 5, 1)`.

## Common fund-name gotchas

- **Berkshire Hathaway** is `Berkshire+Hathaway` — not "Berkshire Hathaway Inc".
- **GQG Partners** is `GQG+Partners+LLC` (note the LLC).
- **Pershing Square** is `Pershing+Square+Capital+Management` (full registered name).
- **Akre** sometimes shows as `Akre+Capital+Management` even though the founder
  Chuck Akre retired — the firm name persists.
- **Atreides** has `+Lp` at the end — the entity registration.

## Aggregation gotchas

- **GOOG vs GOOGL.** Always merge into single "Alphabet" ticker. The two
  share classes have nearly identical economics; some funds hold one, some
  the other, some both. If you don't merge, Alphabet's true consensus rank
  drops misleadingly.
- **Berkshire share classes** (BRK.A vs BRK.B) — same merging principle if
  any fund holds Berkshire as a position.
- **Mastercard / Visa** — these are different companies, do NOT merge.
  But if a user asks "what's the consensus on payments", you might combine
  them as a thematic basket.
- **AUM-weighted aggregation is ALWAYS dominated by the largest fund.** If
  Berkshire ($274B) is in the set, its top holdings will dominate the
  $-value rankings even when no other fund holds them. Always show the
  equal-weighted view alongside.
- **Funds with zero overlap** — if the user picks a set of funds with very
  different mandates (e.g. quant + value + tech-only), the aggregation can
  show no stock held by more than 2–3 funds. That's a real signal: smart
  money disagrees in this set.

## When to refuse / pivot

- **Real-time portfolio decisions.** Remind the user that 13F data has a
  45+ day lag and that hedge funds may have already exited positions you're
  seeing. Don't position the analysis as actionable trading advice.
- **Investment recommendations.** Don't tell the user to buy or sell. Frame
  output as informational: "these are the consensus picks among smart money."
- **Performance claims that can't be verified.** Hedge fund net returns are
  generally private. Only a few public vehicles (PSH.L for Pershing Square,
  Berkshire's own stock, mutual fund versions like AKREX) have verifiable
  long-term track records. Don't fabricate fund return numbers.

## Stale data refresh

- 13F filings update each quarter (Feb, May, Aug, Nov filings)
- Star ratings change as performance updates
- AUM moves with markets
- If running this skill on the same fund 3+ months later, expect different numbers

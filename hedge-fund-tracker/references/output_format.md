# Markdown Output Format

When the user wants markdown rather than HTML, use this structure.

## 1. Quick header

```markdown
# Hedge Fund Tracker — [date]

**Funds analyzed:** N (combined 13F AUM $XXX.XB)
**Criteria:** ≥4★ rating · $10B+ AUM · top-3 >30%
**Source:** HedgeFollow.com (13F long-equity data only)
```

## 2. Fund comparison table

```markdown
| Fund | Manager | AUM (13F) | Rating | Top-3 % | 3-yr | 5-yr | Passes? |
|------|---------|-----------|--------|---------|------|------|---------|
| Sanders Capital | Lewis Sanders | $86.8B | ★★★★★ (4.8) | 30.4% | 28.8% | n/a | ✅ |
| Point72 | Steven Cohen | $75.2B | ★★★★★ (5.0) | ~6% | 41.7% | ~18% | ❌ Top-3 |
```

## 3. Equal-weighted aggregation table

```markdown
## Equal-Weighted Top Positions

| # | Ticker | Company | Avg % | # Funds Holding |
|---|--------|---------|-------|-----------------|
| 1 | GOOGL | Alphabet | 4.75% | 8 of 10 |
| 2 | MSFT  | Microsoft | 4.14% | 6 of 10 |
| 3 | META  | Meta | 3.73% | 6 of 10 |
```

## 4. Top consensus picks — fund-by-fund detail

For each of the top 5 consensus picks, show which funds hold it and at what %:

```markdown
### #1 — GOOGL (Alphabet) — held by 8 of 10 funds

| Fund | % of Portfolio |
|------|----------------|
| Pershing Square | 12.46% |
| Sanders Capital | 11.53% |
| Generation IM | 5.40% |
| ... | ... |

*Not held by:* Berkshire Hathaway, Akre Capital
```

## 5. Caveats footer

Always end with:

```markdown
---

**Caveats:**
- HedgeFollow data is 13F-only — long U.S. equity, no shorts/bonds/options/cash
- "AUM" = 13F long-equity AUM, not true firm AUM (often 1.3–2x larger)
- "Performance" on HedgeFollow is a simulation of the top-20 holdings, not actual fund net returns
- 13F filings have a 45-day lag and quarterly cadence
```

## Style notes

- Use ★ filled / ☆ empty (or just count) for ratings
- ✅ for pass, ❌ for fail, ⚠️ for partial/borderline
- Keep tables wide enough to be scannable but not so wide they wrap on mobile
- Always show "X of N funds" rather than just count — gives the user immediate context

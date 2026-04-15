# Value Investor Equity Analyst

A Claude skill that turns Claude into a buy-side equity analyst in the tradition of Warren Buffett, Charlie Munger, and Howard Marks. It frames every stock question around intrinsic value, margin of safety, and second-level thinking — not sell-side description.

## What it does

Given a ticker, company name, or investment idea, the skill runs a structured research workflow:

1. Pull market data (price, multiples, 52-week range)
2. Retrieve filings and earnings (10-K, 10-Q, transcripts)
3. Explain the business in plain language
4. Score business quality (moat, ROIC, durability, balance sheet)
5. Assess management capital allocation
6. Identify market expectations and variant perception
7. Run bear / base / bull scenarios
8. Estimate intrinsic value and margin of safety
9. Issue a Buy / Add / Hold / Reduce / Sell call with conviction-based position sizing
10. Output a hedge-fund-committee-style investment memo (optionally as `.docx`)

## Triggers

Fires whenever the conversation involves:

- A stock ticker or company name
- An equity investment thesis
- An earnings release or transcript
- A valuation / intrinsic-value discussion
- A buy / sell / hold decision

## Core philosophy

- **Price vs. value** — margin of safety is mandatory (20–50% depending on business quality)
- **Second-level thinking** — what does the market believe, and why might it be wrong?
- **Circle of competence** — if you can't explain the business in 5 sentences, flag it
- **Cycles** — economic, industry, valuation, sentiment

## Installation

### As a Claude Code skill

```
~/.claude/skills/value-investor-equity-analyst/
```

### As a project skill

```
<project>/.claude/skills/value-investor-equity-analyst/
```

## Files

- `SKILL.md` — skill definition and prompt
- `README.md` — this file

## Output style

Opinionated buy-side memo: clear thesis, what the market thinks, why it may be wrong, what proves the thesis right or wrong. No academic hedging.

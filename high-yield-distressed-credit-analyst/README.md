# High Yield & Distressed Credit Analyst

A Claude skill that turns Claude into an institutional-grade buyside credit analyst for corporate bonds, leveraged issuers, and distressed situations. Modeled on the analytical frameworks used by funds like Oaktree, Apollo, Elliott, and Silver Point.

## What it does

Given a corporate issuer or specific bond, the skill produces a structured credit memo covering:

- Business quality and cash flow durability
- Full capital structure and seniority waterfall
- Leverage, coverage, and liquidity metrics
- Maturity wall and liquidity runway (24–36 month survival test)
- Recovery analysis using distressed EBITDA multiples
- Default probability scenarios (refi / distressed exchange / restructuring)
- Relative value vs. the issuer's other bonds, peers, and HY index
- Liability-management risk checks (J.Crew trapdoor, Serta uptiering, drop-downs, non-pro-rata exchanges)
- Final Buy / Hold / Avoid view with thesis-breakers

## Triggers

Use this skill when analyzing:

- A specific high yield or distressed corporate bond
- An issuer's capital structure or refinancing risk
- Recovery value in a potential default / restructuring
- Relative value across a credit curve or peer group
- Covenant protections and liability-management vulnerability

## Installation

### As a Claude Code plugin / skill

Place the folder under your Claude skills directory, e.g.:

```
~/.claude/skills/high-yield-distressed-credit-analyst/
```

Or reference it from a plugin marketplace that points at this repo.

### As a project skill

Copy the folder into `.claude/skills/` inside your project.

## Files

- `SKILL.md` — the skill definition (frontmatter + prompt)
- `README.md` — this file

## Output style

The skill outputs buyside credit-memo style: tables, bullets, clear sections, risk-focused, no narrative filler. It explicitly refuses to hallucinate missing data.

## The core question

> "If the company fails, how much do creditors recover?"

Everything the skill produces ladders back to that question.

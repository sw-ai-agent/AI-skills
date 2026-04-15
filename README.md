# AI Skills

A collection of Claude skills for institutional-grade financial analysis.

## Skills

| Skill | Purpose |
|---|---|
| [high-yield-distressed-credit-analyst](./high-yield-distressed-credit-analyst) | Buy-side HY & distressed credit analyst (Oaktree / Apollo / Elliott style). Default probability, recovery value, liquidity runway, relative value. |
| [value-investor-equity-analyst](./value-investor-equity-analyst) | Buffett / Munger / Marks style equity analyst. Intrinsic value, margin of safety, second-level thinking, scenario analysis. |

## Layout

Each skill is a folder containing:

```
<skill-name>/
├── SKILL.md    # the skill prompt + frontmatter (name, description)
└── README.md   # human-facing overview
```

## Using these skills with Claude Code

Drop a skill folder into:

```
~/.claude/skills/<skill-name>/
```

…or into a project at `.claude/skills/<skill-name>/`. Claude Code will discover any folder containing a `SKILL.md` and load the frontmatter. The `description` field determines when the skill auto-triggers.

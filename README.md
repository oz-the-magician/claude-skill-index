# Claude Skill Index

A bilingual (RU / EN) catalogue of Claude skills I have reviewed for code and licence, then installed.
Every entry links to the author's original repository. Nothing from those repositories is re-hosted here.

**Site:** https://oz-the-magician.github.io/claude-skill-index/

## How an entry gets here

1. I find a skill.
2. Its code and licence are reviewed: scripts, network calls, API keys, autonomous loops, redistribution terms.
3. The skill is installed in Claude.
4. A card is added to `skills/<id>.yml`.
5. GitHub Actions validates every card and rebuilds the site. If a card is invalid, the site is not updated and the run shows why.

## Card format

```yaml
id: humanizer                 # must match the file name
name: Humanizer
skill: humanizer              # name used in Claude
author: Siqi Chen
source: https://github.com/blader/humanizer
license: MIT
license_caveat: false         # true when the licence limits use or redistribution
tags: [text]                  # motion, ui, web, style, game2d, video, slides, text, engineering
where: web                    # web = web and desktop; desktop = needs code execution
needs: [text]                 # text, node, ffmpeg
load: 0                       # 0 to 5, local machine load
checked: 11.10.2026
summary: { ru: "...", en: "..." }
prompt:  { ru: "...", en: "..." }
note:    { ru: "...", en: "..." }
pairs: ""
```

Check locally with `pip install pyyaml && python scripts/build.py --check`.

## Licences

- Site code (`site/`, `scripts/`, `.github/`): MIT, see `LICENSE`.
- Card texts (`skills/`) and this README: CC BY 4.0, see `LICENSE-CONTENT`.
- The skills themselves belong to their authors under their own licences, shown on each card.
  A check date covers the version reviewed on that day, not later ones.

#!/usr/bin/env python3
"""Validate skill cards in skills/*.yml and build the static site into _site/.

Usage:
  python scripts/build.py            # validate + build
  python scripts/build.py --check    # validate only (used on pull requests)
"""
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
TEMPLATE = ROOT / "site" / "index.template.html"
OUT = ROOT / "_site"

TAGS = {"motion", "ui", "web", "style", "game2d", "video", "slides", "text"}
WHERE = {"web", "desktop"}
NEEDS = {"text", "node", "ffmpeg"}
REQUIRED = ["id", "name", "skill", "author", "source", "license", "tags", "where",
            "needs", "load", "checked", "summary", "prompt", "note"]
BILINGUAL = ["summary", "prompt", "note"]
DATE = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")


def validate(path, card, seen):
    errs = []
    for k in REQUIRED:
        if k not in card or card[k] in (None, "", []):
            errs.append(f"missing field '{k}'")
    if errs:
        return errs
    if card["id"] != path.stem:
        errs.append(f"id '{card['id']}' must match file name '{path.stem}'")
    if card["id"] in seen:
        errs.append(f"duplicate id '{card['id']}'")
    if not str(card["source"]).startswith("https://github.com/"):
        errs.append("source must be an https://github.com/ link to the author's repository")
    bad = set(card["tags"]) - TAGS
    if bad:
        errs.append(f"unknown tags {sorted(bad)}; allowed {sorted(TAGS)}")
    if card["where"] not in WHERE:
        errs.append(f"where must be one of {sorted(WHERE)}")
    bad = set(card["needs"]) - NEEDS
    if bad:
        errs.append(f"unknown needs {sorted(bad)}; allowed {sorted(NEEDS)}")
    if not isinstance(card["load"], int) or not 0 <= card["load"] <= 5:
        errs.append("load must be an integer from 0 to 5")
    if not DATE.match(str(card["checked"])):
        errs.append("checked must look like DD.MM.YYYY")
    for k in BILINGUAL:
        v = card[k]
        if not isinstance(v, dict) or not v.get("ru") or not v.get("en"):
            errs.append(f"'{k}' needs both ru and en text")
        elif len(v["ru"]) > 400 or len(v["en"]) > 400:
            errs.append(f"'{k}' text is longer than 400 characters")
    return errs


def load_cards():
    cards, problems, seen = [], [], set()
    for path in sorted(SKILLS.glob("*.yml")):
        try:
            card = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            problems.append(f"{path.name}: invalid YAML ({e})")
            continue
        errs = validate(path, card, seen)
        if errs:
            problems += [f"{path.name}: {e}" for e in errs]
        else:
            seen.add(card["id"])
            cards.append(card)
    return cards, problems


def to_page(card):
    return {
        "id": card["id"], "name": card["name"], "skill": card["skill"],
        "author": card["author"], "src": card["source"], "lic": card["license"],
        "warn": bool(card.get("license_caveat")), "tags": card["tags"],
        "where": card["where"], "needs": card["needs"], "load": card["load"],
        "checked": str(card["checked"]),
        "sum": [card["summary"]["ru"], card["summary"]["en"]],
        "prompt": [card["prompt"]["ru"], card["prompt"]["en"]],
        "risk": [card["note"]["ru"], card["note"]["en"]],
        "pairs": card.get("pairs") or "",
    }


def main():
    cards, problems = load_cards()
    if problems:
        print("Card validation failed:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"{len(cards)} cards valid")
    if "--check" in sys.argv:
        return
    data = "const S=" + json.dumps([to_page(c) for c in cards], ensure_ascii=False) + ";"
    html = TEMPLATE.read_text(encoding="utf-8")
    if "/*SKILLS*/" not in html:
        sys.exit("template is missing the /*SKILLS*/ marker")
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(
        "<!doctype html>\n<html lang=\"ru\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">"
        "</head><body>\n" + html.replace("/*SKILLS*/", data) + "\n</body></html>\n",
        encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print(f"built {OUT / 'index.html'}")


if __name__ == "__main__":
    main()

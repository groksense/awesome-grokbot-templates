#!/usr/bin/env python3
"""Verify the shipped README is an Awesome list of live Grok Bot templates."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")

TOP10 = [
    "93gOz3op1UQdBdbekQFLK",  # Dr Eggbot
    "3mf-UN4mGnCp8DbPBnW5u",  # Home robots
    "br5f3C4mc75QCMEHaszXd",  # tinkabot
    "ZRxm1O9tmizOhriV7GiWL",  # Grok Build
    "Vk0cnF2c364QxNv-Xip1M",  # Clip Bot
    "Ub3T7usX-c6yRQibQq83P",  # loops
    "0VC1XzREXRFGe0hVo-JEG",  # Be Happier
    "VjbtJ_qTdzbhJGmXdvTIc",  # Lennybot
    "j7B5LHnEIPTuPQZxxQwpx",  # Master
    "uY_7s1TZILVzUeJ9lLOx9",  # Tradbot
]
DEAD = [
    "nGEBqtXuN-klNcPPyoR3S",
    "QhfOU5SJ60U8g2x2pUFcT",
    "UMCdNlqEH7USe3eOznd1U",
    "IHA3Iiw7vhSa5lmE82o-p",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if "https://awesome.re/badge.svg" not in README or "https://awesome.re)" not in README.replace(
        "https://awesome.re/badge.svg)](https://awesome.re)", "https://awesome.re)"
    ):
        if "https://awesome.re" not in README:
            fail("README missing official Awesome badge linking to awesome.re")
    if "![Awesome](https://awesome.re/badge.svg)](https://awesome.re)" not in README:
        fail("README missing official Awesome badge markdown")

    m = re.search(r"^## .+", README, re.M)
    if not m or m.group(0) != "## Contents":
        fail(f"first ## heading must be Contents, got {m.group(0) if m else None!r}")

    if not (ROOT / "CONTRIBUTING.md").is_file() and not (ROOT / "contributing.md").is_file():
        fail("missing CONTRIBUTING.md")

    license_files = list(ROOT.glob("LICENSE*")) + list(ROOT.glob("license*"))
    if not license_files:
        fail("missing LICENSE")
    lic = license_files[0].read_text(encoding="utf-8")
    if "CC0" not in lic and "Creative Commons" not in lic:
        fail("LICENSE is not CC0 / Creative Commons")

    if re.search(r"\[!\[.*(?:build|ci|travis|actions).*\]\(http", README, re.I):
        fail("README must not carry a CI badge")

    for slug in TOP10:
        if f"https://x.ai/bot/{slug}" not in README:
            fail(f"missing top-10 slug {slug}")

    for slug in DEAD:
        if slug in README:
            fail(f"known-dead slug listed as live: {slug}")

    n = len(re.findall(r"https://x\.ai/bot/[A-Za-z0-9_-]+", README))
    if n < 10:
        fail(f"expected >=10 template share links, got {n}")

    print(f"ok: {n} share links, Contents first, CC0, top-10 present, dead slugs absent")


if __name__ == "__main__":
    main()

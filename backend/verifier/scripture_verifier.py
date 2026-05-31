import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

BIBLE_PATH = ROOT / "data" / "processed_bible.json"

with open(
    BIBLE_PATH,
    "r",
    encoding="utf-8"
) as f:
    verses = json.load(f)

verse_lookup = {}

for verse in verses:
    key = (
        verse["book"].lower(),
        verse["chapter"],
        verse["verse"]
    )

    verse_lookup[key] = verse


def get_verse(
    book: str,
    chapter: int,
    verse: int
):
    key = (
        book.lower(),
        chapter,
        verse
    )

    return verse_lookup.get(key)


def parse_reference(
    reference: str
):
    pattern = r"(.+?)\s+(\d+):(\d+)"

    match = re.match(
        pattern,
        reference.strip()
    )

    if not match:
        return None

    return (
        match.group(1),
        int(match.group(2)),
        int(match.group(3))
    )
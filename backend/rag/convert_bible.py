#convert_bible.py
import json
from pathlib import Path

BOOK_MAPPING = {
    "gn": "Genesis",
    "ex": "Exodus",
    "lv": "Leviticus",
    "nm": "Numbers",
    "dt": "Deuteronomy",
    "js": "Joshua",
    "jg": "Judges",
    "rt": "Ruth",
    "1sm": "1 Samuel",
    "2sm": "2 Samuel",
    "1ki": "1 Kings",
    "2ki": "2 Kings",
    "1ch": "1 Chronicles",
    "2ch": "2 Chronicles",
    "ezr": "Ezra",
    "ne": "Nehemiah",
    "et": "Esther",
    "job": "Job",
    "ps": "Psalms",
    "pr": "Proverbs",
    "ec": "Ecclesiastes",
    "so": "Song of Solomon",
    "is": "Isaiah",
    "jr": "Jeremiah",
    "lm": "Lamentations",
    "ez": "Ezekiel",
    "dn": "Daniel",
    "hs": "Hosea",
    "jl": "Joel",
    "am": "Amos",
    "ob": "Obadiah",
    "jn": "Jonah",
    "mi": "Micah",
    "na": "Nahum",
    "hk": "Habakkuk",
    "zp": "Zephaniah",
    "hg": "Haggai",
    "zc": "Zechariah",
    "ml": "Malachi",
    "mt": "Matthew",
    "mk": "Mark",
    "lk": "Luke",
    "jo": "John",
    "ac": "Acts",
    "rm": "Romans",
    "1co": "1 Corinthians",
    "2co": "2 Corinthians",
    "gl": "Galatians",
    "ep": "Ephesians",
    "php": "Philippians",
    "cl": "Colossians",
    "1th": "1 Thessalonians",
    "2th": "2 Thessalonians",
    "1tm": "1 Timothy",
    "2tm": "2 Timothy",
    "tt": "Titus",
    "phm": "Philemon",
    "hb": "Hebrews",
    "jm": "James",
    "1pe": "1 Peter",
    "2pe": "2 Peter",
    "1jo": "1 John",
    "2jo": "2 John",
    "3jo": "3 John",
    "jd": "Jude",
    "re": "Revelation"
}

ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_PATH = ROOT / "data" / "en_kjv.json"
OUTPUT_PATH = ROOT / "data" / "processed_bible.json"

with open(INPUT_PATH, "r", encoding="utf-8-sig") as f:
    bible = json.load(f)

processed = []

for book in bible:

    book_name = BOOK_MAPPING.get(
        book["abbrev"],
        book["abbrev"]
    )

    for chapter_num, chapter in enumerate(
        book["chapters"],
        start=1
    ):

        for verse_num, verse_text in enumerate(
            chapter,
            start=1
        ):

            processed.append(
                {
                    "book": book_name,
                    "chapter": chapter_num,
                    "verse": verse_num,
                    "text": verse_text
                }
            )

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        processed,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Total verses: {len(processed)}")
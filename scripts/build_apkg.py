#!/usr/bin/env python3
"""Build a single .apkg file from all flashcard CSVs for one-click Anki import."""

import csv
import hashlib
import genanki
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Stable IDs derived from names (genanki needs consistent ints)
def stable_id(name: str) -> int:
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)

# --- Model definitions (must match Anki note types) ---

BASIC_MODEL = genanki.Model(
    stable_id('MathVisual-Basic'),
    'MathVisual-Basic',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'Hint'},
        {'name': 'Example'},
        {'name': 'Source'},
        {'name': 'Tags'},  # stored as field but also applied as tags
    ],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Front}}<br><br><small style="color:#888">{{Hint}}</small>',
        'afmt': '{{FrontSide}}<hr id="answer">{{Back}}'
               '<br><br>{{#Example}}<b>Example:</b> {{Example}}{{/Example}}',
    }],
    css='.card { font-family: arial; font-size: 20px; text-align: left; }'
)

CLOZE_MODEL = genanki.Model(
    stable_id('MathVisual-Cloze'),
    'MathVisual-Cloze',
    fields=[
        {'name': 'Text'},
        {'name': 'Source'},
        {'name': 'Example'},
        {'name': 'Tags'},
    ],
    templates=[{
        'name': 'Cloze',
        'qfmt': '{{cloze:Text}}',
        'afmt': '{{cloze:Text}}<br><br>'
               '{{#Example}}<b>Example:</b> {{Example}}{{/Example}}',
    }],
    model_type=genanki.Model.CLOZE,
    css='.card { font-family: arial; font-size: 20px; text-align: left; } '
        '.cloze { font-weight: bold; color: blue; }'
)

# --- Deck hierarchy: one deck per module ---

MODULE_NAMES = {
    'mt2501': 'MT2501 – Linear Algebra',
    'mt2506': 'MT2506 – Vector Calculus',
    'mt2508': 'MT2508 – Statistics',
    'ec2001': 'EC2001 – Microeconomics',
}


def parse_csv(filepath: Path) -> list[list[str]]:
    """Read CSV, return list of rows."""
    with open(filepath, encoding='utf-8') as f:
        return list(csv.reader(f))


def build_package():
    decks = {}
    for module, display_name in MODULE_NAMES.items():
        deck = genanki.Deck(stable_id(f'deck-{module}'), display_name)
        decks[module] = deck

    card_count = 0
    csv_files = sorted(ROOT.glob('*/flashcards/*.csv'))

    for csvpath in csv_files:
        module = csvpath.parts[-3]  # e.g. mt2508
        if module not in decks:
            print(f"  Skipping unknown module: {csvpath}")
            continue

        is_cloze = 'cloze' in csvpath.name
        model = CLOZE_MODEL if is_cloze else BASIC_MODEL
        rows = parse_csv(csvpath)

        for row in rows:
            if not row or all(c.strip() == '' for c in row):
                continue

            # Extract tags from last field — keep both full tag and split parts
            tags_field = row[-1].strip() if row else ''
            tags = []
            if tags_field:
                tags = [tags_field]  # Full hierarchical tag (e.g. mt2506::tut1::method::velocity)
                parts = tags_field.split('::')
                if len(parts) > 1:
                    tags.extend(parts)  # Individual parts for Anki filtering

            note = genanki.Note(
                model=model,
                fields=row,
                tags=tags,
                guid=genanki.guid_for(csvpath.name, '|'.join(row[:2])),
            )
            decks[module].add_note(note)
            card_count += 1

    package = genanki.Package(list(decks.values()))
    outpath = ROOT / 'flashcards.apkg'
    package.write_to_file(str(outpath))
    print(f"Built {outpath.name}: {card_count} cards across {len(decks)} decks")


if __name__ == '__main__':
    build_package()

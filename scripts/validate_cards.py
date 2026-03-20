#!/usr/bin/env python3
"""Validate flashcard CSVs for format errors before Anki import.

Usage:
    python scripts/validate_cards.py                  # Validate all CSVs
    python scripts/validate_cards.py path/to/file.csv # Validate specific file
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BASIC_FIELDS = 6   # Front, Back, Hint, Example, Source, Tags
CLOZE_FIELDS = 4   # Text, Source, Example, Tags

TAG_PATTERN = re.compile(r'^[a-z0-9]+::(tut|ec|lab|ch)\d+::(method|exercise)::\w+$')
CLOZE_PATTERN = re.compile(r'\{\{c\d+::')
MAX_FRONT_WORDS = 25


def count_words_outside_math(text: str) -> int:
    """Count words excluding LaTeX math expressions."""
    # Remove display math
    text = re.sub(r'\\\[.*?\\\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    # Remove inline math
    text = re.sub(r'\\\(.*?\\\)', '', text)
    text = re.sub(r'\$.*?\$', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    words = text.split()
    return len(words)


def check_latex_delimiters(text: str) -> list[str]:
    """Check for unbalanced LaTeX delimiters."""
    errors = []
    for open_d, close_d in [('\\(', '\\)'), ('\\[', '\\]')]:
        opens = text.count(open_d)
        closes = text.count(close_d)
        if opens != closes:
            errors.append(f"Unbalanced {open_d}...{close_d}: {opens} opens, {closes} closes")

    # Check braces (rough — only count unescaped)
    depth = 0
    for ch in text:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        if depth < 0:
            errors.append("Extra closing brace '}'")
            break
    if depth > 0:
        errors.append(f"Unclosed braces: {depth} unmatched '{{' ")

    # Check for double backslashes (common mistake)
    double_bs = re.findall(r'\\\\(frac|theta|phi|alpha|beta|gamma|delta|sigma|mu|lambda|nabla|partial|mathbf|operatorname|sqrt|sum|prod|int|lim|sin|cos|tan|log|ln|exp|inf|sup|max|min|det|dim|ker|text|mathrm|hat|bar|vec|dot|ddot|tilde|quad|qquad|left|right|big|Big|bigg|Bigg)', text)
    if double_bs:
        errors.append(f"Double backslash before LaTeX commands (should be single): \\\\{', \\\\'.join(set(double_bs))}")

    return errors


def validate_csv(filepath: Path) -> list[str]:
    """Validate a single CSV file. Returns list of error messages."""
    errors = []
    is_cloze = 'cloze' in filepath.name
    expected_fields = CLOZE_FIELDS if is_cloze else BASIC_FIELDS

    try:
        with open(filepath, encoding='utf-8') as f:
            rows = list(csv.reader(f))
    except Exception as e:
        return [f"Cannot read CSV: {e}"]

    if not rows:
        return [f"Empty CSV file"]

    for i, row in enumerate(rows, 1):
        if not row or all(c.strip() == '' for c in row):
            continue

        # Field count
        if len(row) != expected_fields:
            errors.append(f"Row {i}: Expected {expected_fields} fields, got {len(row)}")
            continue  # Skip further checks if field count is wrong

        # Tag format
        tag = row[-1].strip()
        if not tag:
            errors.append(f"Row {i}: Missing tag")
        elif not TAG_PATTERN.match(tag):
            errors.append(f"Row {i}: Tag '{tag}' doesn't match format course::assessmentN::type::subtopic")

        # Cloze-specific checks
        if is_cloze:
            text = row[0]
            if not CLOZE_PATTERN.search(text):
                errors.append(f"Row {i}: Cloze card missing {{{{c1::...}}}} syntax")
        else:
            # Basic card: check front word count
            front = row[0]
            wc = count_words_outside_math(front)
            if wc > MAX_FRONT_WORDS:
                errors.append(f"Row {i}: Front has {wc} words (max {MAX_FRONT_WORDS})")

        # LaTeX checks on all text fields
        for j, field in enumerate(row[:-1]):  # Skip tag field
            latex_errors = check_latex_delimiters(field)
            for err in latex_errors:
                errors.append(f"Row {i}, field {j+1}: {err}")

    return errors


def main():
    if len(sys.argv) > 1:
        files = [Path(arg) for arg in sys.argv[1:]]
    else:
        files = sorted(ROOT.glob('*/flashcards/*.csv'))

    if not files:
        print("No CSV files found.")
        sys.exit(0)

    total_errors = 0
    total_cards = 0

    for filepath in files:
        errors = validate_csv(filepath)
        # Count cards
        try:
            with open(filepath, encoding='utf-8') as f:
                cards = sum(1 for row in csv.reader(f) if row and any(c.strip() for c in row))
        except Exception:
            cards = 0

        total_cards += cards

        if errors:
            print(f"\n{filepath.relative_to(ROOT)}  ({cards} cards, {len(errors)} errors)")
            for err in errors:
                print(f"  - {err}")
            total_errors += len(errors)
        else:
            print(f"  {filepath.relative_to(ROOT)}  ({cards} cards) OK")

    print(f"\n{'='*50}")
    print(f"Total: {total_cards} cards, {total_errors} errors")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == '__main__':
    main()

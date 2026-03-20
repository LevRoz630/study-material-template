---
name: flashcards
description: Generate Anki flashcard CSVs from tutorial sheets, example classes, or lecture chapters
argument-hint: <module/assessment e.g. math101/tut2>
user-invocable: true
---

# Flashcard Generation

Generate exhaustive Anki flashcard CSVs for the specified assessment or chapter.

**Input:** `$ARGUMENTS` — module and assessment (e.g. `math101/tut2`, `econ201/ec1`, `phys301/ch3`)

## Step 1: Locate Sources

Parse `$ARGUMENTS` to identify module and assessment:
- `math101/tut2` → module `math101`, tutorial 2
- `econ201/ec1` → module `econ201`, example class 1
- `phys301/ch3` → module `phys301`, lecture chapter 3

Read the assessment file and identify which lecture-note chapters are relevant. Only read those chapters — avoid loading all chapters to prevent context overflow.

If a solutions file exists in `solutions/`, read it too — solutions define exactly what skills the cards should teach.

## Step 2: Identify Skills & Knowledge

For each question in the assessment:
1. What definition/theorem/formula is needed?
2. What computational procedure is used?
3. What are the common mistakes?

Every exercise card must have a corresponding method card teaching the underlying technique.

## Step 3: Generate Cards

### MathVisual-Basic (6 fields)

```
Front, Back, Hint, Example, Source, Tags
```

- Front: ≤ 25 words (excluding math). Ask ONE thing
- Back: ≤ 3 concise lines
- Hint: brief memory trigger
- Example: concrete worked instance
- Source: lecture chapter or assessment reference
- Tags: `course::assessmentN::type::subtopic`

### MathVisual-Cloze (4 fields)

```
Text, Source, Example, Tags
```

- Use `{{c1::hidden}}` — always `c1` for ALL deletions on a card
- Good for multi-step derivations, formula components

### LaTeX Rules
- `\( ... \)` inline, `\[ ... \]` display
- **Single backslashes only**: `\frac`, `\theta`, `\nabla` (NOT `\\frac`)
- CSV does not use backslash escaping

### Tag Format
`course::assessmentN::type::subtopic`
- `type` = `method` (reusable technique) or `exercise` (specific worked problem)
- Examples: `math101::tut1::method::velocity`, `econ201::ec1::exercise::consistency`

## Step 4: Write Output

Save to `module/flashcards/`:
- `{assessment}_basic_cards.csv` — basic cards
- `{assessment}_cloze_cards.csv` — cloze cards

CSV: UTF-8, quoted fields, HTML allowed, no header row.

## Step 5: Validate

Run `python scripts/validate_cards.py` on the generated CSVs to check for format errors. Fix any issues found.

## Card Quality Checklist
- [ ] Each card tests ONE fact
- [ ] Method card exists for every exercise card's underlying technique
- [ ] Front ≤ 25 words (excluding math)
- [ ] LaTeX uses single backslashes
- [ ] Tags follow `course::assessmentN::type::subtopic` format
- [ ] Cloze cards use `c1` for all deletions
- [ ] Field count: 6 for basic, 4 for cloze

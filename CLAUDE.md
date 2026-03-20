# Study Material Template — Agent Instructions

Study-material repo: lecture notes, papers, tutorials, and readings converted to markdown, then distilled into Anki flashcards.

## Project Layout

```
{module_code}/              # e.g. math101, econ201, phys301
├── lecture-notes/          # Chapter-by-chapter markdown (split from source.pdf)
├── exercises/              # Problem sheets (examples classes + tutorials)
├── homework/               # Homework assignments
├── class-tests/            # Class test papers and prep notes
├── notes/                  # Revision guides and course summaries
├── flashcards/             # CSV output for Anki import
├── solutions/              # Tutorial solutions with method explanations
├── revision/               # Revision materials
└── practicals/             # Practical exercises
papers/                     # Research papers and readings
scripts/
├── pdf2md.py               # PDF → sectioned markdown (uses pdftotext)
├── build_apkg.py           # CSV flashcards → .apkg package (uses genanki)
└── validate_cards.py       # CSV flashcard validation (fields, LaTeX, cloze, tags)
```

Not every module needs every subdirectory — adapt the layout to fit your course structure (e.g. use `tutorials/`, `labs/`, `textbook/` if that matches better).

## Environment

- **Python venv:** `.venv/` — activate with `source .venv/bin/activate`
- **Dependencies:** `pip install -r requirements.txt` → markitdown (PDF/DOCX conversion), genanki (Anki packages)
- **System tools:** pandoc (org/LaTeX/structured text), pdftotext (used by pdf2md.py)

## Document Conversion

Convert source documents to clean markdown. Prefer the right tool for the job:

| Source format | Tool | Command |
|---|---|---|
| PDF (general) | markitdown | `markitdown input.pdf > output.md` |
| PDF (lecture notes, split by chapter) | pdf2md.py | `python scripts/pdf2md.py input.pdf output_dir/` |
| DOCX | markitdown | `markitdown input.docx > output.md` |
| HTML | markitdown | `markitdown input.html > output.md` |
| Org-mode / LaTeX | pandoc | `pandoc input.org -o output.md` |

When converting:
- **Preserve hyperlinks** — never strip URLs from source material
- **Preserve document structure** — headings, lists, tables
- **Clean up artifacts** — remove page numbers, headers/footers, orphaned line breaks from PDF column layout
- After conversion, review output and fix formatting issues (broken tables, split paragraphs, garbled LaTeX)

## Flashcard Generation

### Card Principles
- Each card tests ONE fact, operation, or visual concept
- Front/Text ≤ 25 words (excluding math). Back ≤ 3 concise lines
- Use LaTeX: `\( ... \)` inline, `\[ ... \]` display — **single backslashes** only (`\frac` not `\\frac`)
- More source material = more cards. Be exhaustive

### Card Types
- **Method cards** (tag: `method`) — reusable definitions, formulas, procedures
- **Exercise cards** (tag: `exercise`) — specific worked problems from assessments

### Note Types

**MathVisual-Basic** fields: `Front, Back, Hint, Example, Source, Tags`

**MathVisual-Cloze** fields: `Text, Source, Example, Tags`
- Cloze syntax: `{{c1::hidden}}` — use `c1` for ALL deletions on a card

### Output
- Two CSVs per topic: `{chapter}_basic_cards.csv`, `{chapter}_cloze_cards.csv`
- UTF-8, quoted fields, HTML allowed, no header row
- Tags format: `{module}::assessmentN::type::subtopic` (e.g. `{module_code}::tut1::method::basis_vectors`)

## Skills (Slash Commands)

Use these instead of working from scratch — they encode all formatting rules and quality checks:

| Skill | Purpose | Example |
|---|---|---|
| `/convert` | PDF/DOCX → clean markdown | `/convert {module_code}/source.pdf lecture-notes/` |
| `/flashcards` | Generate Anki CSVs from assessment | `/flashcards {module_code}/tut2` |
| `/solve` | Write worked tutorial solutions | `/solve {module_code}/tut3` |
| `/revise` | Create revision guide for a tutorial | `/revise {module_code}/tut1` |

## Validation

After generating flashcards, always run:
```bash
python scripts/validate_cards.py                    # all CSVs
python scripts/validate_cards.py path/to/file.csv   # specific file
```
Checks: field counts, LaTeX delimiters, cloze syntax, tag format, word limits.

## Workflow

1. User provides source material (PDF, DOCX, HTML, or pasted text)
2. Convert to clean markdown using `/convert` or the appropriate tool above
3. Place in the correct module directory following the layout above
4. If solutions needed: generate with `/solve`, reading lecture notes + tutorial sheet
5. If flashcards requested: generate with `/flashcards`, then validate with `validate_cards.py`
6. Build .apkg with `python scripts/build_apkg.py` if packaging for Anki import

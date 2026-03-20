# Study Material Template

Convert lecture notes and tutorials to markdown, then turn them into Anki flashcards. Uses Claude Code skills to handle the formatting rules so you don't have to remember them.

## Setup

```bash
git clone https://github.com/YOUR_USER/study-material-template.git my-study-materials
cd my-study-materials
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

You also need `pdftotext` (from poppler-utils) and `pandoc` installed on your system.

## Skills

| Skill | What it does |
|---|---|
| `/convert` | PDF/DOCX to clean markdown. Picks the right tool, cleans up artifacts. |
| `/flashcards` | Generates Anki flashcard CSVs from a tutorial or chapter. |
| `/solve` | Writes step-by-step worked solutions for a tutorial sheet. |
| `/revise` | Creates a revision guide with theory, worked examples, and common mistakes. |

## Scripts

| Script | What it does |
|---|---|
| `scripts/pdf2md.py` | Splits a PDF into per-chapter markdown files. |
| `scripts/build_apkg.py` | Builds an `.apkg` from all flashcard CSVs. Edit `MODULE_NAMES` dict for your modules. |
| `scripts/validate_cards.py` | Checks flashcard CSVs for format errors (field counts, LaTeX, tags). |

## Adding a module

```bash
mkdir -p mymodule/{lecture-notes,exercises,solutions,flashcards}
```

Convert your PDFs with `/convert`, generate flashcards with `/flashcards`, validate with `validate_cards.py`. The `example-module/` directory shows what the output looks like.

## Workflow

```
PDF  →  /convert  →  markdown  →  /flashcards  →  CSVs  →  build_apkg.py  →  .apkg  →  Anki
```

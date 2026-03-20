# Study Material Template

A template repository for converting lecture notes, papers, and tutorials to clean markdown and generating Anki flashcards using Claude Code skills. Set up a structured workflow for any course: drop in PDFs, convert them to markdown with `/convert`, generate exhaustive flashcard decks with `/flashcards`, and build `.apkg` packages ready for one-click Anki import.

## Use This Template

**Option A — GitHub template:**
1. Click **"Use this template"** on the GitHub repo page to create your own copy.

**Option B — Fork:**
1. Fork this repo and clone it locally.

**Option C — Manual:**
```bash
git clone https://github.com/YOUR_USER/study-material-template.git my-study-materials
cd my-study-materials
```

## Directory Structure

```
study-material-template/
├── .claude/skills/
│   ├── convert/SKILL.md        # /convert — PDF/DOCX to markdown
│   ├── flashcards/SKILL.md     # /flashcards — generate Anki CSVs
│   ├── solve/SKILL.md          # /solve — worked tutorial solutions
│   └── revise/SKILL.md         # /revise — revision guides
├── scripts/
│   ├── pdf2md.py               # PDF → sectioned markdown
│   ├── build_apkg.py           # CSV → .apkg Anki package
│   └── validate_cards.py       # Validate flashcard CSV format
├── example-module/             # Sample module showing the pattern
│   ├── lecture-notes/
│   ├── exercises/
│   ├── solutions/
│   └── flashcards/
├── CLAUDE.md                   # Agent instructions for Claude Code
├── requirements.txt
└── .gitignore
```

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **markitdown** — PDF and DOCX to markdown conversion
- **genanki** — Anki `.apkg` package builder

### 3. Install system tools

You also need these command-line tools:

- **pdftotext** — used by `pdf2md.py` for PDF text extraction
  - Ubuntu/Debian: `sudo apt install poppler-utils`
  - macOS: `brew install poppler`
- **pandoc** — for Org-mode and LaTeX conversion
  - Ubuntu/Debian: `sudo apt install pandoc`
  - macOS: `brew install pandoc`

## Skills Reference

These Claude Code slash commands encode all formatting rules and quality checks:

| Skill | Purpose | Usage |
|---|---|---|
| `/convert` | Convert PDF/DOCX to clean markdown | `/convert mymodule/source.pdf lecture-notes/` |
| `/flashcards` | Generate Anki flashcard CSVs from an assessment | `/flashcards mymodule/tut2` |
| `/solve` | Write step-by-step worked solutions | `/solve mymodule/tut3` |
| `/revise` | Create a revision guide for a tutorial or topic | `/revise mymodule/tut1` |

## Scripts Reference

| Script | Purpose | Usage |
|---|---|---|
| `pdf2md.py` | Split a PDF into per-chapter markdown files | `python scripts/pdf2md.py input.pdf output_dir/` |
| `build_apkg.py` | Build an `.apkg` file from all flashcard CSVs | `python scripts/build_apkg.py` |
| `validate_cards.py` | Validate flashcard CSVs (fields, LaTeX, tags) | `python scripts/validate_cards.py [file.csv]` |

> **Note:** `build_apkg.py` contains a `MODULE_NAMES` dictionary that maps directory names to Anki deck names. Edit this dictionary to match your own modules before running.

## How to Add a New Module

### 1. Create the module directories

```bash
mkdir -p mymodule/{lecture-notes,exercises,solutions,flashcards}
```

### 2. Convert your PDFs to markdown

Drop your lecture note PDFs into the module directory, then convert:

```bash
# Split a textbook into per-chapter markdown files
python scripts/pdf2md.py mymodule/textbook.pdf mymodule/lecture-notes/

# Or use the /convert skill in Claude Code
/convert mymodule/textbook.pdf lecture-notes/
```

### 3. Add exercise sheets

Convert tutorial/exercise PDFs the same way:

```bash
/convert mymodule/tutorial1.pdf exercises/
```

### 4. Generate flashcards

Once you have markdown lecture notes and exercises:

```bash
/flashcards mymodule/tut1
```

This generates two CSVs in `mymodule/flashcards/`:
- `tut1_basic_cards.csv` — question-and-answer cards
- `tut1_cloze_cards.csv` — fill-in-the-blank cards

### 5. Validate and build

```bash
# Check for format errors
python scripts/validate_cards.py mymodule/flashcards/tut1_basic_cards.csv

# Build the .apkg file for Anki import
python scripts/build_apkg.py
```

### 6. Update `build_apkg.py`

Edit the `MODULE_NAMES` dictionary in `scripts/build_apkg.py` to include your module:

```python
MODULE_NAMES = {
    'mymodule': 'My Module – Course Title',
}
```

## Example Workflow: PDF to Anki

```
lecture-notes.pdf
       │
       ▼
  /convert  ───►  mymodule/lecture-notes/01-introduction.md
                   mymodule/lecture-notes/02-methods.md
                   ...
       │
       ▼
  /flashcards  ──►  mymodule/flashcards/ch1_basic_cards.csv
                     mymodule/flashcards/ch1_cloze_cards.csv
       │
       ▼
  validate_cards.py  ──►  fix any errors
       │
       ▼
  build_apkg.py  ──►  flashcards.apkg  ──►  Import into Anki
```

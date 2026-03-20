---
name: convert
description: Convert a PDF or DOCX file to clean markdown and place it in the correct module directory
argument-hint: <file-path> [output-dir]
user-invocable: true
---

# Document Conversion

Convert a source document to clean markdown.

**Input:** `$ARGUMENTS` — path to source file, optionally followed by output directory

## Step 1: Identify Format & Tool

| Source format | Tool | Command |
|---|---|---|
| PDF (lecture notes, split by chapter) | pdf2md.py | `python scripts/pdf2md.py input.pdf output_dir/` |
| PDF (general) | markitdown | `markitdown input.pdf > output.md` |
| DOCX | markitdown | `markitdown input.docx > output.md` |
| HTML | markitdown | `markitdown input.html > output.md` |
| Org-mode / LaTeX | pandoc | `pandoc input.org -o output.md` |

For lecture-note PDFs (multi-chapter), prefer `pdf2md.py` as it splits into per-chapter files.

## Step 2: Run Conversion

Activate the venv first: `source .venv/bin/activate`

Run the appropriate conversion command. Place output in the correct module directory:
- Lecture notes → `module/lecture-notes/`
- Tutorial sheets → `module/tutorial-classes/`
- Example classes → `module/example-classes/`

## Step 3: Clean Up Output

Review the generated markdown and fix:
- **Page numbers / headers / footers** — remove repeated title lines and page numbers
- **Hyphenated line breaks** — rejoin words split across lines (`mathe-\nmatics` → `mathematics`)
- **Broken tables** — reconstruct from garbled column output
- **Split paragraphs** — rejoin sentences orphaned by PDF column layout
- **Garbled LaTeX** — fix missing spaces around operators, broken delimiters
- **Preserve hyperlinks** — never strip URLs from source material
- **Preserve document structure** — headings, lists, tables

## Step 4: Verify

Read the final output and confirm it renders as clean, readable markdown with correct LaTeX.

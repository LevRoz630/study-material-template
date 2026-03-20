#!/usr/bin/env python3
"""
Convert PDF to sectioned markdown files.

Usage:
    python pdf2md.py <input.pdf> <output_dir>

Automatically detects document type (lecture notes vs papers) and splits accordingly.
"""

import subprocess
import sys
import re
from pathlib import Path

# Chapter patterns for lecture notes - matches "1 Introduction" style headers
CHAPTER_PATTERNS = [
    r'^\s*chapter\s+(\d+)[:\.]?\s*(.*?)\s*$',
    r'^(\d+)\s+([A-Z][A-Za-z\s,\-]+)\s*$',  # "1 Introduction"
]

# Paper section patterns
PAPER_PATTERNS = [
    (r'^\s*abstract\s*$', '01-abstract', 'Abstract'),
    (r'^\s*\d*\.?\s*introduction\s*$', '02-introduction', 'Introduction'),
    (r'^\s*\d*\.?\s*(methods?|methodology)\s*$', '03-methods', 'Methods'),
    (r'^\s*\d*\.?\s*(results?|findings?)\s*$', '04-results', 'Results'),
    (r'^\s*\d*\.?\s*(discussion|analysis)\s*$', '05-discussion', 'Discussion'),
    (r'^\s*\d*\.?\s*(conclusions?|summary)\s*$', '06-conclusion', 'Conclusion'),
    (r'^\s*references?\s*$', '07-references', 'References'),
]


def extract_text(pdf_path: Path) -> str:
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ['pdftotext', '-layout', str(pdf_path), '-'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {result.stderr}")
    return result.stdout


def detect_document_type(text: str) -> str:
    """Detect if document is lecture notes or a paper."""
    text_lower = text.lower()

    # Count chapter mentions
    chapter_count = len(re.findall(r'\bchapter\s+\d', text_lower))

    # Count paper section mentions
    paper_keywords = ['abstract', 'methodology', 'results', 'discussion', 'references']
    paper_count = sum(1 for kw in paper_keywords if kw in text_lower[:5000])

    if chapter_count >= 2:
        return 'lecture'
    elif paper_count >= 3:
        return 'paper'
    else:
        return 'lecture'  # Default to lecture-style chapter splitting


def identify_chapter(line: str, next_line: str = "") -> tuple[str, str] | None:
    """Check if line is a chapter header. Returns (filename, title) or None."""
    line_stripped = line.strip()
    if not line_stripped or len(line_stripped) > 100:
        return None

    # Match "Chapter X" with title on next line
    chapter_match = re.match(r'^\s*chapter\s+(\d+)\s*$', line_stripped, re.IGNORECASE)
    if chapter_match:
        num = chapter_match.group(1).zfill(2)
        title = next_line.strip() if next_line.strip() else f"Chapter {num}"
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        return (f"{num}-{slug}", title)

    # Match "X Title" format (e.g., "1 Introduction")
    for pattern in CHAPTER_PATTERNS[1:]:  # Skip first pattern (handled above)
        match = re.match(pattern, line_stripped, re.IGNORECASE)
        if match:
            num = match.group(1).zfill(2)
            title = match.group(2).strip() if match.group(2) else f"Chapter {num}"
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            if slug:
                return (f"{num}-{slug}", title)

    return None


def identify_paper_section(line: str) -> tuple[str, str] | None:
    """Check if line is a paper section header."""
    line_stripped = line.strip()
    if not line_stripped or len(line_stripped) > 80:
        return None

    for pattern, filename, title in PAPER_PATTERNS:
        if re.match(pattern, line_stripped, re.IGNORECASE):
            return (filename, title)

    return None


def get_next_nonempty_line(lines: list[str], start: int) -> tuple[str, int]:
    """Get next non-empty line and its index."""
    for i in range(start, min(start + 5, len(lines))):  # Look up to 5 lines ahead
        if lines[i].strip():
            return lines[i], i
    return "", start


def split_into_sections(text: str, doc_type: str) -> dict[str, tuple[str, list[str]]]:
    """Split text into sections based on document type."""
    sections = {}
    current_file = '00-front-matter'
    current_title = 'Front Matter'
    current_lines = []

    lines = text.split('\n')

    if doc_type == 'lecture':
        i = 0
        while i < len(lines):
            line = lines[i]
            # Check for "Chapter X" pattern
            if re.match(r'^\s*chapter\s+\d+\s*$', line.strip(), re.IGNORECASE):
                next_line, title_idx = get_next_nonempty_line(lines, i + 1)
                section_info = identify_chapter(line, next_line)
                if section_info:
                    if current_lines or current_file == '00-front-matter':
                        sections[current_file] = (current_title, current_lines)
                    current_file, current_title = section_info
                    current_lines = []
                    i = title_idx  # Skip to after title line
            else:
                current_lines.append(line)
            i += 1
    else:
        for line in lines:
            section_info = identify_paper_section(line)
            if section_info:
                if current_lines or current_file == '00-front-matter':
                    sections[current_file] = (current_title, current_lines)
                current_file, current_title = section_info
                current_lines = []
            else:
                current_lines.append(line)

    if current_lines:
        sections[current_file] = (current_title, current_lines)

    return sections


def clean_content(lines: list[str]) -> str:
    """Clean up extracted content."""
    text = '\n'.join(lines)

    # Collapse excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Remove standalone page numbers (e.g. "  42  " or "Page 12")
    text = re.sub(r'^\s*(?:Page\s+)?\d{1,4}\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)

    # Rejoin hyphenated line-break words (e.g. "mathe-\nmatics" → "mathematics")
    text = re.sub(r'(\w)-\n\s*(\w)', r'\1\2', text)

    # Remove repeated header/footer lines (same short line appearing 3+ times)
    line_counts: dict[str, int] = {}
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped and len(stripped) < 80:
            line_counts[stripped] = line_counts.get(stripped, 0) + 1
    repeated = {line for line, count in line_counts.items() if count >= 3 and len(line) < 60}
    if repeated:
        filtered = []
        for line in text.split('\n'):
            if line.strip() not in repeated:
                filtered.append(line)
        text = '\n'.join(filtered)

    # Collapse blank lines again after removals
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def write_sections(sections: dict, output_dir: Path):
    """Write sections to markdown files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, (title, lines) in sorted(sections.items()):
        content = clean_content(lines)
        if not content and filename != '00-front-matter':
            continue

        md_path = output_dir / f"{filename}.md"
        md_content = f"# {title}\n\n{content}\n"
        md_path.write_text(md_content)
        print(f"  {md_path.name} ({len(content)} chars)")


def convert_single(pdf_path: Path, output_path: Path):
    """Convert PDF to a single markdown file without splitting."""
    text = extract_text(pdf_path)
    content = clean_content(text.split('\n'))

    # Try to extract title from first non-empty line
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    title = lines[0] if lines else pdf_path.stem

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"# {title}\n\n{content}\n")
    print(f"  {output_path.name} ({len(content)} chars)")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    output = Path(sys.argv[2])

    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)

    # If output ends with .md, do single file conversion
    if output.suffix == '.md':
        print(f"Converting: {pdf_path} -> {output}")
        convert_single(pdf_path, output)
        print("Done!")
        return

    # Otherwise, split into sections
    output_dir = output
    print(f"Extracting: {pdf_path}")
    text = extract_text(pdf_path)

    doc_type = detect_document_type(text)
    print(f"Detected: {doc_type}")

    sections = split_into_sections(text, doc_type)
    print(f"Found {len(sections)} sections")

    print(f"Writing to: {output_dir}")
    write_sections(sections, output_dir)
    print("Done!")


if __name__ == '__main__':
    main()

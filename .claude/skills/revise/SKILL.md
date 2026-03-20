---
name: revise
description: Create a revision guide for a tutorial or topic with theory, worked examples, and common mistakes
argument-hint: <module/tutorialN or topic e.g. mt2506/tut1>
user-invocable: true
---

# Revision Guide

Create a revision guide for the specified tutorial or topic.

**Input:** `$ARGUMENTS` — module and tutorial/topic (e.g. `mt2506/tut1`, `mt2501/diagonalisation`)

## Step 1: Read Sources

1. Read the tutorial sheet from `module/tutorial-classes/`
2. Read relevant lecture-note chapters (only the ones needed — check "Related chapters:" if present)
3. Read example classes if they cover the same topics
4. Read existing solutions if available in `module/solutions/`

## Step 2: Create Revision Guide

Save as `module/tutorial-classes/XX-tutorial-revision.md` (matching the tutorial number).

### Content Structure

#### Core Topics
For each topic covered in the tutorial:
- Clear explanation of the underlying theory
- The key formulas and definitions, fully stated
- Visual/diagrammatic aids using ASCII where helpful (coordinate diagrams, sketches, function graphs)

#### Worked Examples
- One fully worked example per question type — similar to but not identical to the tutorial questions
- Show the complete step-by-step method
- Give concrete numeric examples when concepts are abstract

#### Quick Reference
- Table mapping each tutorial question → the technique/formula needed to solve it
- One-line summary per question

#### Common Mistakes
- Typical errors students make on these topics
- Sign errors, domain restrictions, misapplied formulas
- "Watch out for..." warnings

### Formatting
- Use LaTeX math: `$...$` inline, `$$...$$` display
- `\mathbf{}` for vectors, `\frac{}{}` for fractions, `\nabla`, `\partial`
- Never write equations in plain text or code blocks
- Explanations should be detailed enough to solve the tutorial problems without needing the lecture notes

---
name: solve
description: Generate worked tutorial solutions with step-by-step mathematical reasoning
argument-hint: <module/tutorialN e.g. mt2501/tut3>
user-invocable: true
---

# Tutorial Solutions

Generate complete worked solutions for the specified tutorial sheet.

**Input:** `$ARGUMENTS` — module and tutorial (e.g. `mt2501/tut3`, `mt2506/tut2`)

## Step 1: Read Sources

1. Read the tutorial sheet from `module/tutorial-classes/`
2. Read the relevant lecture-note chapters (check "Related chapters:" header if present)
3. Check if solutions already exist in `module/solutions/` — if so, confirm with user before overwriting

## Step 2: Write Solutions

Save as `module/solutions/tutorialN.md`

### Structure per Question

Every question follows this skeleton:

#### Given / Setup
- Restate key information (function, constraints, domain)
- Define shorthand (e.g. "Let $r = \sqrt{x^2 + y^2 + z^2}$")
- Keep brief — just enough to be self-contained

#### Concept (1–2 lines)
- State the relevant definition, theorem, or formula
- Name the proof strategy: direct proof, contradiction, induction, counterexample, case analysis
- Do NOT derive the concept — just name it and write the formula

#### Step-by-step Working
- Number each step or use clear subheadings
- Show every algebraic manipulation that changes the expression's form
- Skip only trivial arithmetic (e.g. $2 \times 3 = 6$)
- Use $\Longrightarrow$ or "so" to connect logical steps
- Show intermediate forms before final simplification

#### Result
- Box final answers with `$\boxed{...}$`
- For "show that" questions: end with explicit confirmation (e.g. "$= 0$ as required $\checkmark$")
- State geometric/physical interpretation if the question asks for one

### Formatting Rules
- LaTeX throughout: `$...$` inline, `$$...$$` display
- Vectors in bold: `$\mathbf{r}$`, `$\mathbf{e}_R$`
- Separate each question with `---`
- Headings: `## Question N`, `### Part (i)`
- Reference earlier results explicitly (e.g. "Using $d\mathbf{r}/dt$ from part (i)...")

### How Much Detail

**Always include:** formula being applied, every differentiation/integration/algebraic step, intermediate simplifications, final boxed answer, constraint checking

**Keep minimal:** concept explanations (name the formula, don't derive it), physical interpretation (one sentence unless asked), motivation

**Omit:** full derivations of standard results, lengthy prose between steps, restatement of things already shown

## Checklist
- [ ] Every part of every question is answered
- [ ] Each answer starts by identifying the method/formula used
- [ ] All working shown step-by-step with no gaps
- [ ] Final answers boxed
- [ ] "Show that" questions end with explicit confirmation
- [ ] Earlier results referenced, not re-derived
- [ ] LaTeX renders correctly (matched braces, correct delimiters)
- [ ] Constraints and domains respected (e.g. $t \geq 0$)

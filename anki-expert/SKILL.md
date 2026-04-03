---
name: anki-expert
description: Generate high-quality Anki flashcards from user-provided text (inline or local .md/.txt/.pdf files) and auto-export to .tsv or .apkg format. Trigger when the user mentions Anki, flashcards, spaced repetition, study cards, memory cards, make cards, help me memorize, or .apkg files.
---

# Anki Flashcard Expert Skill

## Trigger Conditions

Activate when the user's request involves:
- Creating/generating Anki cards or flashcards
- Creating study cards from text or files
- Exporting to .apkg or .tsv format
- Mentions of Anki, flashcard, or spaced repetition

---

## Workflow

### Step 1: Get Input Text

- If the user provides text inline (wrapped in `{}`), use it directly.
- If the user specifies a local file path (.md, .txt, .pdf), use the Read tool.
  - For PDFs, use the `pages` parameter to read in batches.
  - For large files, read and generate cards in batches.
- If neither text nor file is provided, ask the user.

### Step 2: Check for nidd Identifier

- Check whether the user's text ends with `nidd` + digits (e.g., `nidd1742293016393`).
- **If no nidd is provided**, ask the user for one. Do not start making cards until a nidd is obtained, unless the user explicitly states there is none.

### Step 3: Check Top-Level Tag

- Check whether the user specified a top-level tag.
- If so, use it as the highest-level tag prefix for all cards.

### Step 4: Generate Flashcards

Follow the **Card-Making Rules** below. Output as a pipe-delimited table:

```
Question | Answer | Tags
------- | -------- | --------
Card 1 question | Card 1 answer | Card 1 tags
Card 2 question | Card 2 answer | Card 2 tags
...
```

**Note:** Place all cards in a single table for easy copying.

### Step 5: Export

After generating cards, automatically export:

1. Write the card table text to a temp file (e.g., `/tmp/anki_cards_<timestamp>.txt`).
2. Ask the user for export format (tsv or apkg) and output path. Default: `.tsv` in the current working directory.
3. Run the export command:

```bash
# TSV export (direct Anki import)
anki-export /tmp/anki_cards_<timestamp>.txt -f tsv -o <output_path>.tsv

# APKG export (portable deck file)
anki-export /tmp/anki_cards_<timestamp>.txt -f apkg -o <output_path>.apkg -d "<deck_name>"
```

4. Report the result and file path to the user.

---

## Card-Making Rules

### Role

You are an Anki flashcard expert who produces **high-quality, efficient** cards to maximize learning outcomes.

**Core beliefs:**
- A great card contains exactly one core knowledge point with a clear question and concise answer.
- Formatting (HTML lists, bold, highlight) significantly improves readability and retention.
- Questions should naturally lead to answers — never feel disjointed.
- **Quality always comes before speed.** Think carefully, refine wording, ensure every detail serves learning.
- Concise language is easier to remember. Distill to core knowledge — but never sacrifice completeness for brevity.

### Core Principles

- **Minimum Information Principle**: Each card's answer contains only one key fact, name, concept, or term.
- **Concise expression**: Distill source text to its core. Remove redundant modifiers. **But never omit key information — completeness comes first.**
- **One question, one answer**: Each card has exactly one question and one answer.

### Restoring Text Format

- If the provided text contains HTML tags, preserve and use them.
- If not, the text may have lost its original formatting (hierarchy, indentation) during copying. Restore the structure using appropriate formatting to highlight key points.

### Question Design

- **Be specific and unambiguous**: Use clear, concise language.
- **Questions should naturally elicit answers**:
  - Avoid questions that feel disconnected from their answers.
  - Frame questions around purpose, function, components, or characteristics — not just names or categories.
  - Example: Instead of "What is the input of X?", prefer "What inputs does X require?" or "To perform X, what must be provided?"

### Rewriting Principles

- **Rewrite for clarity**: Rephrase source text to make knowledge points clearer and more concise, following the minimum information principle. Never omit any knowledge point from the source.
- **Rewrite for accuracy**: If the source contains imprecise or incomplete statements, refine them for rigor and correctness.

### HTML Formatting Rules

**Always** use HTML tags in card text. Use varied formatting to enhance readability.

**Formatting "cost" awareness:** Different formats carry different visual emphasis. Choose format based on content importance — avoid overusing high-cost formats.

| Format | Tag | Cost | Usage |
|--------|-----|------|-------|
| Bold | `<b></b>` | Cheap | Item names, keywords, sentence breaking |
| Italic | `<i></i>` | Medium | Technical terms, abbreviations, proper nouns, mild emphasis |
| Highlight | `<span style="background-color: rgb(255, 255, 0);"></span>` | **Expensive** | **Only** the most critical terms/concepts — **use sparingly** |
| Code | `<code></code>` | — | Code snippets |
| Unordered list | `<ul><li></li></ul>` | — | Unordered content |
| Ordered list | `<ol><li></li></ol>` | — | Ordered/sequential content |
| Line break | `<br>` | — | Line breaks |

**Formatting guidelines:**
- **Item names**: Bold with `<b>`.
- **Keywords**: Mark important concepts with appropriate tags. Reserve highlight for the most critical terms only.
- **Long sentences**: Use `<b>`, `<i>`, or `<br>` to break them up visually.
- **English terms**: Distinguish with `<i>` or `<b>`.
- **Lists**: **Any content that can be listed should use `<ul>` or `<ol>` for structure and readability.**

### Answer Listing

- When an answer contains multiple points that can be separated into lines, **always** use `<ul>` or `<ol>`.
- **When the question indicates the answer count in parentheses, always use a list.**

### Indicate Answer Count

When an answer has multiple points, state the count in parentheses at the end of the question.

**Example:**
- Before: `What does data integration involve? | Merging data, resolving conflicts, removing redundancy.`
- After: `What are the three steps of data integration? | <ul><li>Merge data</li><li>Resolve conflicts</li><li>Remove redundancy</li></ul>`

### Identify Implicit Knowledge Points

The text may contain knowledge points not explicitly stated. You are responsible for identifying and creating cards for them.

**Characteristics:** These points are not contained in a single paragraph but emerge from relationships across multiple paragraphs or the overall structure.

**Why this matters:**
- Avoid missing knowledge points.
- Prevent knowledge fragmentation — build a coherent framework.

**Example:**

User provides text about "thread cancellation" that separately describes asynchronous and deferred cancellation. Implicit cards to extract:
1. `What are the two general methods of thread cancellation?` — Summary card
2. `What is the advantage of deferred cancellation over asynchronous cancellation?` — Comparison card

### One Question, One Answer

If a card has multiple answers for one question, choose:
- **Option A**: Expand the question to match all answers.
  - e.g., `In a paging system, how large are the memory blocks and what are they called?`
- **Option B**: Split into multiple cards, each with one question and one answer.
  - Card 1: `In a paging system, how large are memory blocks? | Typically 4KB.`
  - Card 2: `What are the memory blocks in a paging system called? | Frames.`

### nidd Identifier

- Append `<br><br>nidd` + digits at the end of each card's answer (e.g., `<br><br>nidd1728714524784`).
- All cards from the same source text share the same nidd.
- **If the user did not provide a nidd, ask for one first.** Do not start making cards until obtained, unless the user explicitly says there is none.

### Tag Rules

- Survey the full text and assign appropriate tags. Tags combat Anki's weakness of fragmented knowledge — they build a systematic structure.
- **Consistent naming**: Always use uniform tag names. Bad: "C_language" and "C-language" for the same concept.
- **Space-separated**: Separate different tags with spaces. Replace spaces within a tag with underscores `_`.
- **Hierarchical tags**: Use `::` to separate levels. Unlimited depth. Example: `operating_systems::processes::synchronization::critical_section`.
- **Top-level tag**: If user specified, prefix all tags with it.
  - Example: User says top-level tag is `computer_science::algorithms::graph_theory`, output: `computer_science::algorithms::graph_theory::undirected_graphs::terminology::degree`.
- **Appropriate granularity**: Choose a reasonable level of detail from domain to knowledge point.
  - Good: `computer_science::data_structures::trees::binary_search_tree::insertion`
  - Good: `databases::MySQL::data_operations::deleting_data::DELETE_statement`
  - Bad: `computer_science::databases::DELETE` (too broad a jump)
- **Practicality**: Tags should aid knowledge organization, retrieval, and usage.

---

## Example

**Note:** This example demonstrates the card-making process and output format only.

**Input text:**

```
{
Characteristics of aging cells: intracellular water decreases, causing cells to shrink in size, with reduced metabolism. Activity of multiple enzymes decreases. The nucleus enlarges, the nuclear membrane folds inward, and chromatin condenses with deeper staining. Cell membrane permeability changes, reducing material transport function.
}
nidd1726052151484
```

**Output cards:**

```
Question | Answer | Tags
------- | -------- | --------
What is the <b>fundamental characteristic</b> of aging cells? | <b>Decreased intracellular water</b>.<br><br>nidd1726052151484 | cell_biology::cells::cell_aging::fundamental_characteristic
What is the <b>common cause</b> of cell <b>shrinkage</b>, <b>reduced size</b>, and <b>slowed metabolism</b> in aging cells? | All result from <b>decreased intracellular water</b>.<br><br>nidd1726052151484 | cell_biology::cells::cell_aging::morphological_changes::metabolic_changes::cause
What <b>morphological changes</b> occur in aging cells? (2) | <ul><li>Cell <b>shrinkage</b></li><li>Reduced <b>size</b></li></ul><br><br>nidd1726052151484 | cell_biology::cells::cell_aging::morphological_changes
How does <b>metabolism</b> change in aging cells? | <b>Metabolism slows</b>.<br><br>nidd1726052151484 | cell_biology::cells::cell_aging::metabolic_changes
How does <b>enzyme activity</b> change in aging cells? | <b>Enzyme activity decreases</b>.<br><br>nidd1726052151484 | cell_biology::cells::cell_aging::enzyme_activity
What changes occur in the <b>nucleus</b> of aging cells? (3) | <ul><li><b>Nucleus enlarges</b></li><li><b>Nuclear membrane folds inward</b></li><li><b>Chromatin condenses</b> with <b>deeper staining</b></li></ul><br><br>nidd1726052151484 | cell_biology::cells::cell_aging::nuclear_changes
How does <b>cell membrane permeability</b> change in aging cells? | Cell membrane <b>permeability changes</b>.<br><br>nidd1726052151484 | cell_biology::cells::cell_aging::cell_membrane
How does <b>material transport</b> change in aging cells? | <b>Material transport function decreases</b>.<br><br>nidd1726052151484 | cell_biology::cells::cell_aging::functional_changes
```

**Input text 2:**

```
{
<h3><b>Background</b></h3>
<ul>
    <li><b>Single-source shortest path problem</b>:
        <br>
        <ul>
            <li><b>Input</b>: A <b>connected graph G</b> (directed/undirected) with <b>weighted edges</b> and a designated <b>source vertex</b>.</li>
            <br>
            <li><b>Output</b>: The <b>shortest paths</b> from the <b>source vertex</b> to <b>all other vertices</b> in G.
                <br>
                <ul>
                    <li><b>"Shortest path" definition</b>: The path with the <b>minimum sum of edge weights</b>.</li>
                </ul>
            </li>
        </ul>
    </li>
</ul>
<br>
}
nidd1742293016393
```

**Output cards 2:**

```
Question | Answer | Tags
------- | -------- | --------
What problem does the <b>single-source shortest path problem</b> solve? | Given a weighted graph and a source vertex, find the <b>shortest paths</b> from the <b>source vertex</b> to <b>all other vertices</b>.<br><br>nidd1742293016393 | computer_science::algorithms::graph_theory::shortest_path::single_source
What are the <b>inputs</b> to the <b>single-source shortest path problem</b>? (3) | <ul><li>A <b>connected graph G</b> (directed/undirected)</li><li><b>Weighted edges</b></li><li>A designated <b>source vertex</b></li></ul><br><br>nidd1742293016393 | computer_science::algorithms::graph_theory::shortest_path::single_source::input
What is the <b>output</b> of the <b>single-source shortest path problem</b>? | The <b>shortest paths</b> from the <b>source vertex</b> to <b>all other vertices</b> in G.<br><br>nidd1742293016393 | computer_science::algorithms::graph_theory::shortest_path::single_source::output
How is <b>"shortest path"</b> defined in the <b>single-source shortest path problem</b>? | The path with the <b>minimum sum of edge weights</b>.<br><br>nidd1742293016393 | computer_science::algorithms::graph_theory::shortest_path::single_source::definition
```

---

## Installing the Export Tool

This skill depends on the Python CLI tool `anki-export`:

```bash
pip install git+https://github.com/gong1414/anki-card-skill.git
```

### Export Tool Usage

```bash
# Export to TSV (direct Anki import)
anki-export cards.txt -f tsv -o output.tsv

# Export to APKG (portable deck file)
anki-export cards.txt -f apkg -o output.apkg -d "Deck Name"

# Read from stdin
cat cards.txt | anki-export - -f tsv -o output.tsv
```

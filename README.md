# anki-expert

AI-powered Anki flashcard generator — works as a skill/plugin for Claude Code, Cursor, Copilot CLI, Gemini CLI, Codex & OpenCode. Exports to `.tsv` / `.apkg` with HTML formatting, hierarchical tags, and CJK support.

[中文文档](README.zh-CN.md)

## Features

- **Expert flashcard generation** — minimum information principle, structured HTML formatting, hierarchical tags
- **Multiple input sources** — inline text, `.md`, `.txt`, `.pdf` files
- **Auto export** — `.tsv` (direct Anki import) or `.apkg` (portable deck file)
- **Chinese & English** — full CJK and mixed-language support
- **Smart formatting** — cost-aware emphasis (bold / italic / highlight)
- **Hierarchical tags** — multi-level `::` separated tags for structured knowledge
- **nidd tracking** — source identifiers auto-stripped from answers and moved to tags
- **Cloze deletion** — `{{c1::answer}}` syntax for fill-in-the-blank cards

## Installation

### Prerequisites

The export tool `anki-export` must be installed for `.tsv` / `.apkg` export:

```bash
pip install git+https://github.com/gong1414/anki-card-skill.git
```

### Claude Code

```
/plugin marketplace add gong1414/anki-card-skill
/plugin install anki-expert@anki-skill
```

### Cursor

```
/add-plugin anki-expert
```

Or search for "anki-expert" in Cursor's plugin marketplace.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add gong1414/anki-card-skill
copilot plugin install anki-expert@anki-skill
```

### Gemini CLI

```bash
gemini extensions install https://github.com/gong1414/anki-card-skill
```

### Codex

```
Fetch and follow instructions from https://raw.githubusercontent.com/gong1414/anki-card-skill/main/.codex/INSTALL.md
```

### OpenCode

Add to your `opencode.json`:

```json
{
  "plugin": ["anki-expert@git+https://github.com/gong1414/anki-card-skill.git"]
}
```

### Verify

Start a fresh session and try:

```
帮我做 Anki 卡片：
{
进程间通信的主要方式有共享内存和消息传递两种。
}
nidd1234567890
```

If the skill triggers and generates a card table, installation is successful.

## Usage

Tell Claude to create Anki cards:

```
Make Anki cards from this text:
{
衰老细胞的特征是细胞内水分减少，导致细胞萎缩，体积变小，代谢减慢。
}
nidd1726052151484
```

Or from a file:

```
Create Anki flashcards from ./notes/lecture-5.md
```

Claude generates cards following expert rules and automatically exports them.

### CLI Export Tool

```bash
# TSV (Anki direct import)
anki-export cards.txt -f tsv -o output.tsv

# APKG (portable deck file)
anki-export cards.txt -f apkg -o output.apkg -d "My Deck"

# stdin
cat cards.txt | anki-export - -f tsv -o output.tsv
```

## Card Format

Pipe-delimited, three fields:

```
问题 | 答案 | 标签
------- | -------- | --------
衰老细胞的<b>根本特征</b>？ | 细胞内 <b>水分减少</b>。 | 生物学::细胞衰老
```

**HTML tags:** `<b>` bold, `<i>` italic, `<span style="background-color: rgb(255, 255, 0);">` highlight (use sparingly), `<ul>/<ol>` lists, `<code>`, `<br>`

**Tags:** hierarchical with `::` — e.g. `计算机科学::算法::图论::最短路径`

**nidd:** Source tracking identifiers (e.g. `nidd1726052151484`) are automatically stripped from card answers during export and moved to the Anki tags field.

## Troubleshooting

**`anki-export: command not found`**
Ensure the package is installed: `pip install git+https://github.com/gong1414/anki-card-skill.git`. If using a virtual environment, make sure it's activated.

**`Error: no cards parsed from input`**
Check that your input follows the pipe-delimited format: `question | answer | tags`. Each line needs exactly two `|` separators.

**`Error: file not found`**
Verify the input file path. Relative paths are resolved from the current working directory.

## Python API

```python
from anki_skill.parser import parse_cards
from anki_skill.exporters import export_tsv, export_apkg
from pathlib import Path

text = "What is DNA? | Deoxyribonucleic acid | biology::genetics\n"
cards = parse_cards(text)

export_tsv(cards, Path("output.tsv"))
export_apkg(cards, Path("output.apkg"), deck_name="Biology")
```

## License

MIT

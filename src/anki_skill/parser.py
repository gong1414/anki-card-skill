"""Parse pipe-delimited flashcard text into Card objects."""

from __future__ import annotations

from anki_skill.models import Card


def parse_cards(text: str, verbose: bool = False) -> list[Card]:
    """Parse pipe-delimited card text into a list of Card objects.

    Expected format per line:
        question | answer | tags

    Skips header lines (containing '---') and the column header line.
    Uses rightmost-two-pipe split to handle pipes inside HTML content.
    Tags are space-separated within the tags field.
    """
    cards: list[Card] = []
    skipped: list[tuple[int, str]] = []

    for line_num, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        if _is_header_line(line):
            continue

        parts = _split_card_line(line)
        if parts is None:
            skipped.append((line_num, line))
            continue

        question, answer, tags_str = parts
        tags = tags_str.split() if tags_str else []
        cards.append(Card(question=question, answer=answer, tags=tags))

    if verbose and skipped:
        import sys
        for line_num, line in skipped:
            preview = line[:60] + "..." if len(line) > 60 else line
            print(f"  Skipped line {line_num}: {preview}", file=sys.stderr)

    return cards


def _is_header_line(line: str) -> bool:
    """Check if line is a table header or separator."""
    stripped = line.replace("|", "").replace("-", "").strip()
    if not stripped:
        return True
    # Only match when the first pipe-delimited field is exactly "问题" or "question"
    first_field = line.split("|")[0].strip().lower()
    if first_field in ("问题", "question"):
        return True
    return False


def _split_card_line(line: str) -> tuple[str, str, str] | None:
    """Split a card line by the rightmost two pipes.

    This handles cases where question or answer contains pipe characters
    (e.g., inside <code> tags). The tags field (rightmost) never contains
    pipes, and the answer field rarely does, so splitting from the right
    is the safest strategy.
    """
    last_pipe = line.rfind("|")
    if last_pipe == -1:
        return None

    rest = line[:last_pipe]
    tags_str = line[last_pipe + 1 :].strip()

    second_pipe = rest.rfind("|")
    if second_pipe == -1:
        return None

    question = rest[:second_pipe].strip()
    answer = rest[second_pipe + 1 :].strip()

    if not question:
        return None
    # Allow empty answer for cloze deletion cards
    if not answer and "{{c" not in question:
        return None

    return question, answer, tags_str

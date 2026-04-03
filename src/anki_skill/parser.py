"""Parse pipe-delimited flashcard text into Card objects."""

from __future__ import annotations

from anki_skill.models import Card


def parse_cards(text: str) -> list[Card]:
    """Parse pipe-delimited card text into a list of Card objects.

    Expected format per line:
        question | answer | tags

    Skips header lines (containing '---') and the column header line.
    Uses rightmost-two-pipe split to handle pipes inside HTML content.
    Tags are space-separated within the tags field.
    """
    cards: list[Card] = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if _is_header_line(line):
            continue

        parts = _split_card_line(line)
        if parts is None:
            continue

        question, answer, tags_str = parts
        tags = tags_str.split() if tags_str else []
        cards.append(Card(question=question, answer=answer, tags=tags))

    return cards


def _is_header_line(line: str) -> bool:
    """Check if line is a table header or separator."""
    stripped = line.replace("|", "").replace("-", "").strip()
    if not stripped:
        return True
    # Only match exact header rows like "问题 | 答案 | 标签"
    lower = line.lower()
    if (lower.startswith("问题") or lower.startswith("question")) and (
        "答案" in lower or "answer" in lower or "标签" in lower or "tag" in lower
    ):
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

    if not question or not answer:
        return None

    return question, answer, tags_str

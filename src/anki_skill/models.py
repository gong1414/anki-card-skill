"""Data models for Anki flashcards."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Card:
    """A single Anki flashcard with question, answer, and tags."""

    question: str
    answer: str
    tags: list[str] = field(default_factory=list)

    @property
    def tags_string(self) -> str:
        """Tags joined by space, ready for Anki import."""
        return " ".join(self.tags)

    @property
    def answer_plain(self) -> str:
        """Answer with HTML tags stripped, <br> converted to newlines."""
        text = self.answer
        text = re.sub(r"<br\s*/?>", "\n", text)
        text = re.sub(r"<[^>]+>", "", text)
        return text

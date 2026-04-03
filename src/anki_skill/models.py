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
    def nidd(self) -> str:
        """Extract nidd identifier from end of answer, or empty string."""
        m = re.search(r"nidd\d+\s*$", self.answer)
        return m.group(0).strip() if m else ""

    @property
    def answer_clean(self) -> str:
        """Answer with trailing nidd stripped."""
        return re.sub(r"(\s*<br\s*/?>)*\s*nidd\d+\s*$", "", self.answer).rstrip()

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

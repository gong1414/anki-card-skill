import tempfile
from pathlib import Path

from anki_skill.models import Card
from anki_skill.exporters import export_tsv, _sanitize_tsv


def test_sanitize_tsv_removes_tabs():
    assert _sanitize_tsv("hello\tworld") == "hello world"


def test_sanitize_tsv_converts_newlines_to_br():
    assert _sanitize_tsv("line1\nline2") == "line1<br>line2"


def test_sanitize_tsv_removes_carriage_return():
    assert _sanitize_tsv("line1\r\nline2") == "line1<br>line2"


def test_sanitize_tsv_handles_mixed():
    assert _sanitize_tsv("a\tb\nc\r\nd") == "a b<br>c<br>d"


def test_sanitize_tsv_passthrough_clean_string():
    assert _sanitize_tsv("<b>hello</b>") == "<b>hello</b>"


def _sample_cards() -> list[Card]:
    return [
        Card(
            question="<b>Q1</b>",
            answer="A1<br><br>nidd123",
            tags=["tag1::sub"],
        ),
        Card(
            question="Q2",
            answer="<ul><li>A2a</li><li>A2b</li></ul>",
            tags=["tag2", "tag3"],
        ),
    ]


def test_export_tsv_creates_file():
    cards = _sample_cards()
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as f:
        path = Path(f.name)
    export_tsv(cards, path)
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    lines = content.strip().splitlines()
    assert len(lines) == 2  # no header, Anki TSV has no header
    path.unlink()


def test_export_tsv_tab_separated():
    cards = _sample_cards()
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as f:
        path = Path(f.name)
    export_tsv(cards, path)
    content = path.read_text(encoding="utf-8")
    first_line = content.splitlines()[0]
    parts = first_line.split("\t")
    assert len(parts) == 3  # question, answer, tags
    assert parts[0] == "<b>Q1</b>"
    assert parts[1] == "A1"  # nidd stripped from answer
    assert "tag1::sub" in parts[2]
    assert "nidd123" in parts[2]  # nidd moved to tags
    path.unlink()


def test_export_tsv_multiple_tags_space_joined():
    cards = _sample_cards()
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as f:
        path = Path(f.name)
    export_tsv(cards, path)
    content = path.read_text(encoding="utf-8")
    second_line = content.splitlines()[1]
    parts = second_line.split("\t")
    assert parts[2] == "tag2 tag3"
    path.unlink()


from anki_skill.exporters import export_apkg


def test_export_apkg_creates_file():
    cards = _sample_cards()
    with tempfile.NamedTemporaryFile(suffix=".apkg", delete=False) as f:
        path = Path(f.name)
    export_apkg(cards, path, deck_name="Test Deck")
    assert path.exists()
    assert path.stat().st_size > 0
    path.unlink()


def test_export_apkg_default_deck_name():
    cards = _sample_cards()
    with tempfile.NamedTemporaryFile(suffix=".apkg", delete=False) as f:
        path = Path(f.name)
    export_apkg(cards, path)
    assert path.exists()
    path.unlink()


def test_export_apkg_preserves_html():
    cards = [Card(question="<b>Bold Q</b>", answer="<i>Italic A</i>", tags=[])]
    with tempfile.NamedTemporaryFile(suffix=".apkg", delete=False) as f:
        path = Path(f.name)
    export_apkg(cards, path, deck_name="HTML Test")
    assert path.stat().st_size > 0
    path.unlink()

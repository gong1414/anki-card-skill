from anki_skill.models import Card


def test_card_creation():
    card = Card(
        question="<b>单源最短路径问题</b> 旨在解决什么问题？",
        answer="找到 <b>源顶点</b> 到 <b>所有其他顶点</b> 的最短路径。<br><br>nidd1742293016393",
        tags=["计算机科学::算法::图论::最短路径"],
    )
    assert card.question == "<b>单源最短路径问题</b> 旨在解决什么问题？"
    assert "nidd1742293016393" in card.answer
    assert card.tags == ["计算机科学::算法::图论::最短路径"]


def test_card_nidd_extraction():
    card = Card(question="Q", answer="A<br><br>nidd1743696000000", tags=[])
    assert card.nidd == "nidd1743696000000"


def test_card_nidd_empty():
    card = Card(question="Q", answer="No nidd here", tags=[])
    assert card.nidd == ""


def test_card_answer_clean():
    card = Card(question="Q", answer="A<br><br>nidd123", tags=[])
    assert card.answer_clean == "A"


def test_card_answer_clean_no_nidd():
    card = Card(question="Q", answer="Just an answer", tags=[])
    assert card.answer_clean == "Just an answer"


def test_card_tags_as_string():
    card = Card(
        question="Q",
        answer="A",
        tags=["操作系统::进程", "计算机科学"],
    )
    assert card.tags_string == "操作系统::进程 计算机科学"


def test_card_answer_plain_text():
    card = Card(
        question="Q",
        answer="<b>加粗</b> 和 <i>斜体</i><br><br>nidd123",
        tags=[],
    )
    assert card.answer_plain == "加粗 和 斜体\n\nnidd123"


from pathlib import Path
from anki_skill.parser import parse_cards


FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_cards_from_fixture():
    text = (FIXTURES / "sample_cards.txt").read_text(encoding="utf-8")
    cards = parse_cards(text)
    assert len(cards) == 3


def test_parse_cards_first_card():
    text = (FIXTURES / "sample_cards.txt").read_text(encoding="utf-8")
    cards = parse_cards(text)
    assert "根本特征" in cards[0].question
    assert "水分减少" in cards[0].answer
    assert cards[0].tags == ["细胞生物学::细胞::细胞衰老::根本特征"]


def test_parse_cards_multiple_tags():
    text = "Q | A | tag1 tag2::sub\n"
    cards = parse_cards(text)
    assert len(cards) == 1
    assert cards[0].tags == ["tag1", "tag2::sub"]


def test_parse_cards_empty_input():
    assert parse_cards("") == []
    assert parse_cards("问题 | 答案 | 标签\n------|------|------\n") == []


def test_parse_cards_strips_whitespace():
    text = "  Q  |  A  |  tag  \n"
    cards = parse_cards(text)
    assert cards[0].question == "Q"
    assert cards[0].answer == "A"
    assert cards[0].tags == ["tag"]


def test_parse_cards_pipe_in_html():
    """Pipes inside HTML tags should not break parsing."""
    text = 'What is <code>a | b</code>? | Bitwise OR | programming::operators\n'
    cards = parse_cards(text)
    assert len(cards) == 1
    assert "<code>a | b</code>" in cards[0].question
    assert cards[0].answer == "Bitwise OR"

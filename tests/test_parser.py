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
    # nidd stripped, HTML removed
    assert card.answer_plain == "加粗 和 斜体"


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


def test_parse_cards_cjk_full():
    """Full CJK question, answer, and tags."""
    text = "什么是递归？ | 函数调用自身的编程技术。 | 计算机科学::编程::递归\n"
    cards = parse_cards(text)
    assert len(cards) == 1
    assert cards[0].question == "什么是递归？"
    assert "函数调用自身" in cards[0].answer
    assert cards[0].tags == ["计算机科学::编程::递归"]


def test_parse_cards_mixed_cjk_english():
    """Mixed CJK and English content."""
    text = "What is <b>递归</b>? | A function that calls itself (递归调用). | CS::recursion\n"
    cards = parse_cards(text)
    assert len(cards) == 1
    assert "递归" in cards[0].question
    assert "递归调用" in cards[0].answer


def test_parse_cards_emoji_in_content():
    """Emoji characters should not break parsing."""
    text = "What does 🔥 mean? | Fire or excitement. | slang::emoji\n"
    cards = parse_cards(text)
    assert len(cards) == 1
    assert "🔥" in cards[0].question


def test_parse_cards_japanese_korean():
    """Japanese and Korean text."""
    text = "日本語とは？ | 日本で使われる言語です。 | 言語::日本語\n"
    cards = parse_cards(text)
    assert len(cards) == 1
    assert cards[0].tags == ["言語::日本語"]


def test_parse_cards_double_pipe_skipped():
    """Double pipe resulting in empty field should be skipped."""
    text = "Q || | tags\n"
    cards = parse_cards(text)
    assert len(cards) == 0


def test_parse_cards_empty_tags_field():
    """Empty tags field should produce empty tags list."""
    text = "Q | A | \n"
    cards = parse_cards(text)
    assert len(cards) == 1
    assert cards[0].tags == []


def test_parse_cards_no_tags_field():
    """Line with only one pipe (no tags field) should be skipped."""
    text = "Q | A\n"
    cards = parse_cards(text)
    assert len(cards) == 0


def test_parse_cards_multiple_nidd():
    """Only the last nidd should be extracted."""
    card = Card(question="Q", answer="A nidd111<br><br>nidd222", tags=[])
    assert card.nidd == "nidd222"
    assert "nidd111" in card.answer_clean

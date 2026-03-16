from lark import Lark
from ace_language import read_grammar, get_parser, text

def test_ace_simple():
    ace_grammar = read_grammar()
    parser = Lark(ace_grammar)
    parsed = parser.parse(text).pretty()
    assert parsed

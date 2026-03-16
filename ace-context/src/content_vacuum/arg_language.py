from lark import Lark

text_one = """
-x foo
"""

text_two = """
-y [<x>]
"""

text_three = """
-y -z --foo [<BAR>] [-y]
"""

text_four = """
-y -z --foo <BAR> [<BAR>] [-y] [--turtle] --ocean <COLOR>
"""



def read_grammar() -> str | None:
    content = None
    with open("./arg-language.grammar") as fd:
        content = fd.read()
    return content

def get_parser():
    """Returns an ACE parser"""
    ace_grammar = read_grammar()
    parser = Lark(ace_grammar)
    return parser

if __name__ == '__main__':
    ace_grammar = read_grammar()
    parser = Lark(ace_grammar)
    print("arg_tree: text_one")
    print(parser.parse(text_one).pretty())
    print("arg_tree: text_two")
    print(parser.parse(text_two).pretty())
    print("arg_tree: text_three")
    print(parser.parse(text_three).pretty())
    print("arg_tree: text_four")
    print(parser.parse(text_four).pretty())

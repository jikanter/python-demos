from lark import Lark

text = """[shr-1000000] 
When creating DSLs with python, leverage the lark python library to generate those dsls

[ts-10000003]
If you get an error when running lark.Parse, try to make your grammar less ambiguous by pushing tokens up into the parse tree

[per-2342] User prefers to write in a business voice

@@ACE:[cod-12345678]@@ To print a statement in python, use `print(<token>)`

"""

def read_grammar() -> str | None:
    content = None
    with open("./ace.grammar") as fd:
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
    print(parser.parse(text).pretty())




import turtle
text = """
c green blue
fill { repeat 36 {
    f200 l170
    }
}
"""

from lark import Lark

def read_grammar() -> str | None:
    content = None
    with open("./turtle-language.grammar") as fd:
        content = fd.read()
    return content



# the interpreter
def run_instruction(t):
    if t.data == 'change_color':
        turtle.color(*t.children) # we just pass the color names as-is

    elif t.data == 'movement':
        name, number = t.children
        # execute one of the functions for each token
        {
          'f': turtle.fd,
          'b': turtle.bk,
          'l': turtle.lt,
          'r': turtle.rt
        }[name](int(number))

    elif t.data == 'repeat':
        count, block = t.children
        for i in range(int(count)):
            run_instruction(block)

    elif t.data == 'fill':
        turtle.begin_fill()
        run_instruction(t.children[0])
        turtle.end_fill()

    elif t.data == 'code_block':
        for cmd in t.children:
            run_instruction(cmd)

    else:
        raise SyntaxError(f'Unknown instruction: {t.data}')

turtle_grammar = read_grammar()
parser = Lark(turtle_grammar)
#print(parser.parse(text))
#print(parser.parse(text).pretty())

def run_turtle(program) -> None:
    parse_tree = parser.parse(program)

    for inst in parse_tree.children:
        run_instruction(inst)

def main():
    while True:
        code = input('> ')
        try:
            run_turtle(code)
        except Exception as e:
            print(e)

#run_turtle(text)

if __name__ == '__main__':
    main()
"""
Helper functions for interacting with ai agent tool calls.
Note that this is *not* safe for arbitrary input and may lead to code injection vulnerabilities.
"""

import re


def extract_code_from_call(output, tool_name):
    # Pattern to extract the code block
    pattern = rf'"name": "{tool_name}".*?"code":\s*"(.*?)"'
    match = re.search(pattern, output, re.DOTALL)
    if match:
        code = match.group(1)
        return code
    return None

# Try to evaluate the code block
def evaluate_code(code):
    try:
        # Replace newline with space
        code = code.replace('\n', ' ')
        # Evaluate the expression
        result = eval(code)
        return result
    except Exception as e:
        return str(e)

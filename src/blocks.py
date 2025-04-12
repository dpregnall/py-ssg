import re
from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def block_to_block_type(markdown):
    if is_valid_md_header(markdown):
        return BlockType.HEADING.value
    elif is_valid_md_code_block(markdown):
        return BlockType.CODE.value
    elif is_valid_md_quote_block(markdown):
        return BlockType.QUOTE.value
    elif is_valid_md_unordered_list(markdown):
        return BlockType.UNORDERED_LIST.value
    elif is_valid_md_ordered_list(markdown):
        return BlockType.ORDERED_LIST.value
    else:
        return BlockType.PARAGRAPH.value

def is_valid_md_header(line):
    """
    Checks if a single line string is a valid ATX Markdown header.
    e.g., '# Header 1', '## Header 2'
    """
    # Regex: Start (^), 1-6 hashes (#{1,6}), space (\s+), content (.+), End ($)
    header_regex = r"^(#{1,6})\s+(.+)$"
    stripped_line = line.strip() # Strip first
    header_match = re.fullmatch(header_regex, stripped_line)
    return header_match is not None

def is_valid_md_code_block(string):
    code_block_regex =r"^```(?:[a-zA-Z0-9]*)?\n([\s\S]*?)\n^```$"
    code_block_match = re.fullmatch(code_block_regex, string.strip(), re.MULTILINE)
    return code_block_match is not None

def is_valid_md_quote_block(text_block):
    """
    Checks if a string represents a Markdown quote block.
    Each line must start with '> ' or just '>'.
    e.g., '> Line 1\n> Line 2'
    """
    lines = text_block.strip().split('\n')

    if not lines or not text_block.strip():
        return False
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not re.match(r"^>\s?", stripped_line):
             return False

        if not stripped_line and line != ">": # Check original line if stripped is empty
             if not line.strip(): # If the original line was just whitespace/empty
                 return False # Invalid structure

    return True

def is_valid_md_unordered_list(text_block):
    """
    Checks if a string represents a block of Markdown unordered list items.
    Each line must start with '*', '-', or '+' followed by a space and content.
    e.g., '* Item 1\n* Item 2' or '- Item A\n- Item B'
    """
    lines = text_block.strip().split('\n')
    if not lines or not text_block.strip():
        return False

    for line in lines:

        if not re.match(r"^[-*+]\s+.+", line.strip()):
            return False

    return True

def is_valid_md_ordered_list(text_block):
    """
    Checks if a string represents a block of Markdown ordered list items
    where the numbers increment sequentially by one.
    Each line must start with digits, a period, a space, and content.
    e.g., '1. Item 1\n2. Item 2' or '5. Item 5\n6. Item 6'
    """
    lines = text_block.strip().split('\n')
    if not lines or not text_block.strip():
        return False

    expected_number = None
    ordered_list_pattern = r"^(\d+)\.\s+.+"

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        match = re.match(ordered_list_pattern, stripped_line)

        if not match:
            return False # Line doesn't match the pattern 'N. text'

        current_number = int(match.group(1))

        if i == 0:
            expected_number = current_number
        else:
            if current_number != expected_number + 1:
                return False # Numbers are not sequential
            expected_number = current_number

    return True
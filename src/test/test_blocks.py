import unittest
# Assuming your code is in 'blocks.py' in the same directory
from src.blocks import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):

    def test_heading_detection(self):
        """Tests correct identification of different heading levels."""
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING.value)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING.value)
        # Invalid heading (too many #) should be paragraph
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH.value)
        # Invalid heading (no space) should be paragraph
        self.assertEqual(block_to_block_type("#Heading 1"), BlockType.PARAGRAPH.value)

    def test_code_block_detection(self):
        """Tests correct identification of code blocks."""
        code_block_no_lang = "```\nprint('Hello')\n```"
        code_block_with_lang = "```python\ndef test():\n    pass\n```"
        # Test with surrounding whitespace/newlines which should be stripped
        code_block_padded = "\n   ```\nsome code\n```   \n"
        self.assertEqual(block_to_block_type(code_block_no_lang), BlockType.CODE.value)
        self.assertEqual(block_to_block_type(code_block_with_lang), BlockType.CODE.value)
        self.assertEqual(block_to_block_type(code_block_padded), BlockType.CODE.value)
        # Invalid code block (missing fences) should be paragraph
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH.value)
        self.assertEqual(block_to_block_type("code\n```"), BlockType.PARAGRAPH.value)

    def test_quote_block_detection(self):
        """Tests correct identification of quote blocks."""
        single_line_quote = "> This is a quote."
        multi_line_quote = "> Line 1\n> Line 2\n> > Nested maybe (still quote)\n>"
        self.assertEqual(block_to_block_type(single_line_quote), BlockType.QUOTE.value)
        self.assertEqual(block_to_block_type(multi_line_quote), BlockType.QUOTE.value)
        # Invalid quote (missing > on one line) should be paragraph
        invalid_quote = "> Line 1\nLine 2"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH.value)
        # Invalid quote (empty line breaks structure)
        invalid_quote_empty = "> line1\n\n> line3"
        self.assertEqual(block_to_block_type(invalid_quote_empty), BlockType.PARAGRAPH.value)

    def test_unordered_list_detection(self):
        """Tests correct identification of unordered lists."""
        ul_star = "* Item 1\n* Item 2"
        ul_dash = "- Item A\n- Item B"
        ul_plus = "+ Item X\n+ Item Y"
        ul_mixed = "* Star\n- Dash\n+ Plus" # Mixed markers are often allowed per line
        self.assertEqual(block_to_block_type(ul_star), BlockType.UNORDERED_LIST.value)
        self.assertEqual(block_to_block_type(ul_dash), BlockType.UNORDERED_LIST.value)
        self.assertEqual(block_to_block_type(ul_plus), BlockType.UNORDERED_LIST.value)
        self.assertEqual(block_to_block_type(ul_mixed), BlockType.UNORDERED_LIST.value)
        # Invalid list (missing marker) should be paragraph
        invalid_ul = "* Item 1\nItem 2"
        self.assertEqual(block_to_block_type(invalid_ul), BlockType.PARAGRAPH.value)
        # Invalid list (no space after marker) should be paragraph
        invalid_ul_space = "*Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(invalid_ul_space), BlockType.PARAGRAPH.value)

    def test_ordered_list_detection(self):
        """Tests correct identification of sequentially ordered lists."""
        ol_simple = "1. Item 1\n2. Item 2\n3. Item 3"
        ol_start_high = "5. Item 5\n6. Item 6"
        self.assertEqual(block_to_block_type(ol_simple), BlockType.ORDERED_LIST.value)
        self.assertEqual(block_to_block_type(ol_start_high), BlockType.ORDERED_LIST.value)
        # Invalid list (non-sequential) should be paragraph
        invalid_ol_skip = "1. Item 1\n3. Item 3"
        self.assertEqual(block_to_block_type(invalid_ol_skip), BlockType.PARAGRAPH.value)
        # Invalid list (repeating number) should be paragraph
        invalid_ol_repeat = "1. Item 1\n1. Item 1"
        self.assertEqual(block_to_block_type(invalid_ol_repeat), BlockType.PARAGRAPH.value)
        # Invalid list (missing marker) should be paragraph
        invalid_ol_missing = "1. Item 1\nItem 2"
        self.assertEqual(block_to_block_type(invalid_ol_missing), BlockType.PARAGRAPH.value)
        # Invalid list (wrong format) should be paragraph
        invalid_ol_format = "1 Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(invalid_ol_format), BlockType.PARAGRAPH.value)

    def test_paragraph_detection(self):
        """Tests correct identification of paragraphs."""
        plain_text = "This is just a simple paragraph."
        text_with_newlines = "Line one.\nLine two."
        almost_header = "#Not a header"
        almost_list = "-Not a list"
        almost_quote = ">Not really a quote\nJust text"
        self.assertEqual(block_to_block_type(plain_text), BlockType.PARAGRAPH.value)
        self.assertEqual(block_to_block_type(text_with_newlines), BlockType.PARAGRAPH.value)
        self.assertEqual(block_to_block_type(almost_header), BlockType.PARAGRAPH.value)
        self.assertEqual(block_to_block_type(almost_list), BlockType.PARAGRAPH.value)
        self.assertEqual(block_to_block_type(almost_quote), BlockType.PARAGRAPH.value)

    def test_edge_cases(self):
        """Tests edge cases like empty or whitespace strings."""
        empty_string = ""
        whitespace_string = "   \n   \t "
        # Empty or whitespace-only strings should be treated as paragraphs
        self.assertEqual(block_to_block_type(empty_string), BlockType.PARAGRAPH.value)
        self.assertEqual(block_to_block_type(whitespace_string), BlockType.PARAGRAPH.value)

# Standard boilerplate to run tests
if __name__ == '__main__':
    unittest.main()

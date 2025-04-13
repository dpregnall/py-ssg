import unittest, textwrap

from textnode import TextNode, TextType
from parse import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes, 
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title
)

class TestParse(unittest.TestCase):
    def test_code_parse(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        target_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, target_nodes)

    def test_bold_parse(self):
        node = TextNode("This is text with **bold words**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        target_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold words", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, target_nodes)

    def test_parse_fakeout(self):
        node = TextNode("This is text with **bold words**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.BOLD)
        target_nodes = [
            TextNode("This is text with **bold words**.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, target_nodes)

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_mult_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_no_image(self):
        matches = extract_markdown_images(
            "This is text with no image"
        )
        self.assertListEqual([], matches)
    
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_mult_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_no_link(self):
        matches = extract_markdown_links(
            "This is text with no link"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_fakeout(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.TEXT,
                )
            ],
            new_nodes,
        )
    
    def test_split_images_fakeout(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
                    TextType.TEXT,
                )
            ],
            new_nodes,
        )
    
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        target_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, target_nodes)

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        md = textwrap.dedent(md).strip()

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_h1(self):
        md = """
        # Heading 1
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1></div>",
        )

    def test_h2(self):
        md = """
        ## Heading 2
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading 2</h2></div>",
        )
    
    def test_h3(self):
        md = """
        ### Heading 3
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading 3</h3></div>",
        )

    def test_h4(self):
        md = """
        #### Heading 4
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>Heading 4</h4></div>",
        )

    def test_h5(self):
        md = """
        ##### Heading 5
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h5>Heading 5</h5></div>",
        )

    def test_h6(self):
        md = """
        ###### Heading 6
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>Heading 6</h6></div>",
        )

    def test_single_line_blockquote(self):
        md = """
        > Single line quote
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Single line quote</blockquote></div>",
        )
    
    def test_multi_line_blockquote(self):
        md = """
        > This
        > is
        > a
        > multiline
        > quote
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This\nis\na\nmultiline\nquote</blockquote></div>",
        )

    def test_ul(self):
        md = """
        - This
        - is
        - an
        - unordered
        - list
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This</li><li>is</li><li>an</li><li>unordered</li><li>list</li></ul></div>",
        )

    def test_fancy_ul(self):
        md = """
        - This
        - is
        - an
        - unordered
        - list with **bold** items
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This</li><li>is</li><li>an</li><li>unordered</li><li>list with <b>bold</b> items</li></ul></div>",
        )
    
    def test_ol(self):
        md = """
        1. This
        2. is
        3. an
        4. ordered list
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This</li><li>is</li><li>an</li><li>ordered list</li></ol></div>",
        )

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_header_and_paragraphs(self):
        md = """
        # A heading!
        
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
        md = textwrap.dedent(md).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>A heading!</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_extract_header(self):
        md = """
        # A heading!
        
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
        md = textwrap.dedent(md).strip()

        title = extract_title(md)
        target = "A heading!"
        self.assertEqual(title, target)

if __name__ == "__main__":
    unittest.main()
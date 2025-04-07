import unittest

from textnode import TextNode, split_nodes_delimiter, TextType, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node1 = TextNode("dummy text", "bold", "https://google.com")
        text_node2 = TextNode("dummy text", "bold", "https://google.com")
        self.assertEqual(text_node1, text_node2)

    def test_repr(self):
        text_node = TextNode("dummy text", "bold", "https://google.com")
        self.assertEqual(repr(text_node), "TextNode(dummy text, bold, https://google.com)")

    def test_text_eq_fail(self):
        text_node1 = TextNode("dummy text", "bold", "https://google.com")
        text_node2 = TextNode("text", "bold", "https://google.com")
        self.assertNotEqual(text_node1, text_node2)

    def test_text_type_eq_fail(self):
        text_node1 = TextNode("dummy text", "bold", "https://google.com")
        text_node2 = TextNode("dummy text", "italic", "https://google.com")
        self.assertNotEqual(text_node1, text_node2)
    
    def test_url_eq_fail(self):
        text_node1 = TextNode("dummy text", "bold", "https://google.com")
        text_node2 = TextNode("dummy text", "bold", "https://bing.com")
        self.assertNotEqual(text_node1, text_node2)

    def test_no_url_eq_fail(self):
        text_node1 = TextNode("dummy text", "bold")
        text_node2 = TextNode("dummy text", "bold", "https://google.com")
        self.assertNotEqual(text_node1, text_node2)
    
    def test_text_repr_fail(self):
        text_node = TextNode("dummy text", "bold", "https://google.com")
        self.assertNotEqual(repr(text_node), "TextNode(text, bold, https://google.com)")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_multiple_nodes(self):
        node1 = TextNode("This is text with a `code` word", TextType.CODE)
        node2 = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "*", TextType.ITALIC)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a `code` word", TextType.CODE),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_fail(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is a text with an ![image](https://google.com/image.png)"
        nodes = extract_markdown_images(text)
        
        self.assertEqual(nodes, [("image", "https://google.com/image.png")])

    def test_extract_markdown_images_multiple(self):
        text = "This is a text with an ![image](https://google.com/image.png) and another ![image2](https://google.com/image2.png)"
        nodes = extract_markdown_images(text)
        
        self.assertEqual(nodes, [("image", "https://google.com/image.png"), ("image2", "https://google.com/image2.png")])

    def test_extract_markdown_images_fail(self):
        text = "This is a text with a [link](https://google.com/image.png)"
        nodes = extract_markdown_images(text)
        
        self.assertEqual(nodes, [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is a text with a [link](https://google.com)"
        nodes = extract_markdown_links(text)
        
        self.assertEqual(nodes, [("link", "https://google.com")])

    def test_extract_markdown_links_multiple(self):
        text = "This is a text with a [link](https://google.com) and another [link2](https://google.com)"
        nodes = extract_markdown_links(text)
        
        self.assertEqual(nodes, [("link", "https://google.com"), ("link2", "https://google.com")])

    def test_extract_markdown_links_fail(self):
        text = "This is a text with an ![image](https://google.com/image.png)"
        nodes = extract_markdown_links(text)
        
        self.assertEqual(nodes, [])

class TestSplitNodesImages(unittest.TestCase):
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ])
    
    def test_split_nodes_images_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_images_but_not_links(self):
        node = TextNode(
            "This is text with an [link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [node])

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://google.com) and another [second link](https://bing.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://google.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://bing.com"),
        ])
    
    def test_split_nodes_links_no_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_links_but_not_images(self):
        node = TextNode(
            "This is text with an ![image](https://google.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [node])

# class TestTextToTextNodes(unittest.TestCase):
#     def test_text_to_textnodes(self):
#         text = "This is text with a [link](https://google.com) and an ![image](https://google.com/image.png)"
#         nodes = text_to_textnodes(text)
#         self.assertEqual(nodes, [
#             TextNode("This is text with a ", TextType.TEXT),
#             TextNode("link", TextType.LINK, "https://google.com"),
#             TextNode(" and an ", TextType.TEXT),
#             TextNode("image", TextType.IMAGE, "https://google.com/image.png"),
#         ])

#     def test_text_to_textnodes_no_links_or_images(self):
#         text = "This is text with no links or images"
#         nodes = text_to_textnodes(text)
#         self.assertEqual(nodes, [TextNode("This is text with no links or images", TextType.TEXT)])

#     def test_text_to_textnodes_no_text(self):
#         text = ""
#         nodes = text_to_textnodes(text)
#         self.assertEqual(nodes, [])

#     def test_many_types(self):
#         text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
#         nodes = text_to_textnodes(text)
#         self.assertEqual(nodes, [
#             TextNode("This is ", TextType.TEXT),
#             TextNode("text", TextType.BOLD),
#             TextNode(" with an ", TextType.TEXT),
#             TextNode("italic", TextType.ITALIC),
#             TextNode(" word and a ", TextType.TEXT),
#             TextNode("code block", TextType.CODE),
#             TextNode(" and an ", TextType.TEXT),
#             TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
#             TextNode(" and a ", TextType.TEXT),
#             TextNode("link", TextType.LINK, "https://boot.dev"),
#         ])

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is text with a [link](https://google.com) and an ![image](https://google.com/image.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://google.com"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://google.com/image.png"),
        ])

    def test_text_to_textnodes_no_links_or_images(self):
        text = "This is text with no links or images"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is text with no links or images", TextType.TEXT)])

    def test_text_to_textnodes_no_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [])

    def test_many_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

if __name__ == "__main__":
    unittest.main()
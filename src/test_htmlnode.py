import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "Header", None, None)
        node2 = HTMLNode("h1", "Header", None, None)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode("h1", "Header", None, None)
        node2 = HTMLNode("h2", "Header", None, None)
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        props_dict = {"href": "https://www.google.com","target": "_blank",}
        node = HTMLNode("a", "A link", None, props_dict)
        target_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), target_html)


if __name__ == "__main__":
    unittest.main()
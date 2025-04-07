import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        html_node = HtmlNode("p", "dummy text", [HtmlNode("a", "link", props={"href": "https://google.com"})], {"class": "bold"})
        self.assertEqual(repr(html_node), "HtmlNode(p, dummy text, [HtmlNode(a, link, None, {'href': 'https://google.com'})], {'class': 'bold'})")

    def test_props_to_html(self):
        html_node = HtmlNode("p", "dummy text", [HtmlNode("a", "link", props={"href": "https://google.com"})], {"class": "bold"})
        self.assertEqual(html_node.props_to_html(), ' class="bold"')

    def test_props_to_html_no_props(self):
        html_node = HtmlNode("p", "dummy text", [HtmlNode("a", "link", props={"href": "https://google.com"})])
        self.assertEqual(html_node.props_to_html(), "")

    def test_multiple_props_to_html(self):
        html_node = HtmlNode("p", "dummy text", [HtmlNode("a", "link", props={"href": "https://google.com"})], {"class": "bold", "id": "1"})
        self.assertEqual(html_node.props_to_html(), ' class="bold" id="1"')

class TestLeafNode(unittest.TestCase):
    def test_init_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_to_html(self):
        leaf_node = LeafNode("p", "dummy text", {"class": "bold"})
        self.assertEqual(leaf_node.to_html(), '<p class="bold">dummy text</p>')

    def test_to_html_no_tag(self):
        leaf_node = LeafNode(None, "dummy text", {"class": "bold"})
        self.assertEqual(leaf_node.to_html(), 'dummy text')

    def test_to_html_no_props(self):
        leaf_node = LeafNode("p", "dummy text")
        self.assertEqual(leaf_node.to_html(), '<p>dummy text</p>')

    def test_a_to_html(self):
        leaf_node = LeafNode("a", "link", {"href": "https://google.com"})
        self.assertEqual(leaf_node.to_html(), '<a href="https://google.com">link</a>')

class TestParentNode(unittest.TestCase):
    def test_init_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [HtmlNode("a", "link", props={"href": "https://google.com"})])

    def test_init_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None)

    def test_to_html(self):
        parent_node = ParentNode("p", [LeafNode("a", "link", {"href": "https://google.com"})], {"class": "bold"})
        self.assertEqual(parent_node.to_html(), '<p class="bold"><a href="https://google.com">link</a></p>')
    
    def test_to_html_nested(self):
        parent_node = ParentNode("p", [ParentNode("span", [LeafNode("a", "link", {"href": "https://google.com"})], {"class": "bold"})], {"class": "bold"})
        self.assertEqual(parent_node.to_html(), '<p class="bold"><span class="bold"><a href="https://google.com">link</a></span></p>')

    def test_to_html_no_props(self):
        parent_node = ParentNode("p", [LeafNode("a", "link", {"href": "https://google.com"})])
        self.assertEqual(parent_node.to_html(), '<p><a href="https://google.com">link</a></p>')

    def test_to_html_no_children(self):
        parent_node = ParentNode("p", [], {"class": "bold"})
        self.assertEqual(parent_node.to_html(), '<p class="bold"></p>')
    
    def test_example_case(self):
        parent_node = ParentNode("p",[ LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"), ])
        self.assertEqual(parent_node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

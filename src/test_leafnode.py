import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("b", "bold", None)
        node2 = LeafNode("b", "bold", None)
        self.assertEqual(node, node2)

    def test_p_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        target_html = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), target_html)

    def test_a_leaf_to_html(self):
        props_dict = {"href": "https://www.google.com","target": "_blank",}
        node = LeafNode("a", "Click Me!", props_dict)
        target_html = '<a href="https://www.google.com" target="_blank">Click Me!</a>'
        self.assertEqual(node.to_html(), target_html)


if __name__ == "__main__":
    unittest.main()
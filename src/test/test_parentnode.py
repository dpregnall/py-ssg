import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node])
        self.assertEqual(parent_node, parent_node2)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
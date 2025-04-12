from src.htmlnode import HTMLNode
from src.textnode import TextNode, text_node_to_html_node

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        children_html = ""
        for child in self.children:
            if isinstance(child, TextNode):
                children_html += text_node_to_html_node(child).to_html()
            else:
                children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
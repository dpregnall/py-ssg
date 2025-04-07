import re
from enum import Enum
from htmlnode import LeafNode

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    raise Exception("Unsupported text type")

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node)
#             continue
#         if delimiter not in node.text:
#             raise Exception("Delimiter not found") # this is causing issues
        
#         parts = node.text.split(delimiter)

#         new_nodes.extend([
#             TextNode(parts[0], TextType.TEXT),
#             TextNode(parts[1], text_type),
#             TextNode(parts[2], TextType.TEXT),
#         ])

#     return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        
        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))
    
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    if not matches:
        return []
    
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
    if not matches:
        return []
    
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)
        
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for match in matches:
            split_text = text.split(f"![{match[0]}]({match[1]})", 1)    
            new_nodes.extend([
                TextNode(split_text[0], TextType.TEXT),
                TextNode(match[0], TextType.IMAGE, match[1]),
            ])
            text = split_text[1]
            
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
        
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for match in matches:
            split_text = text.split(f"[{match[0]}]({match[1]})", 1)    
            new_nodes.extend([
                TextNode(split_text[0], TextType.TEXT),
                TextNode(match[0], TextType.LINK, match[1]),
            ])
            text = split_text[1]
            
    return new_nodes

def text_to_textnodes(text):
    if not text:
        return []
    nodes = [TextNode(text, TextType.TEXT)]
    try:
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        # print(*nodes, sep="\n")
    except:
        pass
    try:
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    except:
        pass
    try:
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    except:
        pass
    # nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    # nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_images(nodes)
    # print(*nodes, sep="\n")
    nodes = split_nodes_links(nodes)
    print(*nodes, sep="\n")
    return nodes
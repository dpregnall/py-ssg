import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        split = old_node.text.split(delimiter)

        if len(split) == 1: new_nodes.append(old_node)
        if len(split) == 3:
            new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(split[1],text_type))
            new_nodes.append(TextNode(split[2], TextType.TEXT))
        else: 
            continue
    
    return new_nodes

def extract_markdown_images(text):
    regx = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    return re.findall(regx, text)

def extract_markdown_links(text):
    regx = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    return re.findall(regx, text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_images(old_node.text)
        
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        for idx, match in enumerate(matches):
            split_text = text.split(f"![{match[0]}]({match[1]})", 1)    
            new_nodes.extend([
                TextNode(split_text[0], TextType.TEXT),
                TextNode(match[0], TextType.IMAGE, match[1]),
            ])
            text = split_text[1]
            if len(matches) == idx + 1 and text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_links(old_node.text)
        
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        for idx, match in enumerate(matches):
            split_text = text.split(f"[{match[0]}]({match[1]})", 1)    
            new_nodes.extend([
                TextNode(split_text[0], TextType.TEXT),
                TextNode(match[0], TextType.LINK, match[1]),
            ])
            text = split_text[1]
            if len(matches) == idx + 1 and text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    if not text:
        return []
    
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    """
    Splits markdown text into blocks based on double newlines,
    cleaning whitespace and removing empty lines within blocks.

    Args:
        markdown: The input markdown string.

    Returns:
        A list of cleaned markdown blocks.
    """
    if not isinstance(markdown, str):
        # Handle non-string input gracefully
        return []
        # Or raise TypeError("Input must be a string")

    # 1. Split the markdown into potential blocks based on double newlines
    potential_blocks = markdown.split("\n\n")

    cleaned_blocks = []
    for block in potential_blocks:
        # 2. For each potential block:
        #    a. Split it into lines.
        #    b. Strip whitespace from each line.
        #    c. Keep only non-empty lines after stripping.
        cleaned_lines = [line.strip() for line in block.split('\n') if line.strip()]

        # 3. If there are any non-empty lines left after cleaning...
        if cleaned_lines:
            # ...join them back together with single newlines and add to the result.
            cleaned_blocks.append("\n".join(cleaned_lines))

    return cleaned_blocks
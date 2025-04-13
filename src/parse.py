import re

from parentnode import ParentNode
from textnode import TextNode, TextType
from leafnode import LeafNode
from blocks import BlockType, block_to_block_type

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits nodes based on a delimiter, handling multiple occurrences.

    Args:
        old_nodes: A list of TextNode objects.
        delimiter: The string delimiter to split by (e.g., "**", "`").
        text_type: The TextType to assign to the text *between* delimiters.

    Returns:
        A new list of TextNode objects, split appropriately.
    """
    new_nodes = []
    for old_node in old_nodes:
        # Only split nodes that are currently plain text
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue # Skip to the next node if it's not plain text

        # Split the text by the delimiter
        split_parts = old_node.text.split(delimiter)

        # If the delimiter wasn't found, or if splitting resulted in just one
        # (potentially empty) part, add the original node and continue
        if len(split_parts) <= 1:
            # Add the node only if it has text, otherwise discard empty nodes
            if old_node.text:
                new_nodes.append(old_node)
            continue

        # Check for invalid markdown (odd number of delimiters)
        # len(split_parts) - 1 is the number of delimiters found.
        # An odd number of delimiters means unclosed markdown.
        if (len(split_parts) - 1) % 2 != 0:
             raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}' in text '{old_node.text}'")

        # Iterate through the split parts, alternating text types
        for i, part in enumerate(split_parts):
            # Skip empty parts which can occur with leading/trailing/consecutive delimiters
            if not part:
                continue

            # Even indices are outside the delimiter (plain text)
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            # Odd indices are inside the delimiter (special text type)
            else:
                new_nodes.append(TextNode(part, text_type))

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
        return []

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

def markdown_to_html_node(md):
    children_nodes = []

    blocks = markdown_to_blocks(md)
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING.value:
            children_nodes.append(convert_md_header_to_html(block))
        if block_type == BlockType.QUOTE.value:
            children_nodes.append(convert_md_blockquote_to_html(block))
        if block_type == BlockType.UNORDERED_LIST.value:
            children_nodes.append(convert_md_unordered_list_to_html(block))
        if block_type == BlockType.ORDERED_LIST.value:
            children_nodes.append(convert_md_ordered_list_to_html(block))
        if block_type == BlockType.CODE.value:
            children_nodes.append(convert_md_code_block_to_html(block))
        if block_type == BlockType.PARAGRAPH.value:
            children_nodes.append(convert_md_paragraph_to_html(block))

    return ParentNode("div", children_nodes, None)

def convert_md_header_to_html(md):
    split = md.split(' ', 1)
    hash_count = len(split[0])
    
    return LeafNode(f"h{hash_count}", split[1], None)

def convert_md_blockquote_to_html(md):
    lines = md.split("\n")
    new_lines = []
    for line in lines:
        clean_line = line.split(' ', 1)[1] if len(line.split(' ')) != 1 else ""
        new_lines.append(clean_line)
    
    new_lines = "\n".join(new_lines)

    return LeafNode("blockquote", new_lines, None)

def convert_md_unordered_list_to_html(md):
    lines = md.split("\n")
    child_nodes = []
    for line in lines:
        clean_line = line.split(' ', 1)[1]
        text_nodes = text_to_textnodes(clean_line)
        child_nodes.append(ParentNode("li", text_nodes, None))
    
    return ParentNode("ul", child_nodes, None)

def convert_md_ordered_list_to_html(md):
    lines = md.split("\n")
    child_nodes = []
    for line in lines:
        clean_line = line.split(' ', 1)[1]
        text_nodes = text_to_textnodes(clean_line)
        child_nodes.append(ParentNode("li", text_nodes, None))
    
    return ParentNode("ol", child_nodes, None)

def convert_md_paragraph_to_html(md):
    line = " ".join(md.split("\n"))
    text_nodes = text_to_textnodes(line)

    return ParentNode("p", text_nodes, None)

def convert_md_code_block_to_html(md):
    md = md.lstrip('```').rstrip('```')
    lines = md.split("\n")
    new_lines = [line for line in lines if line != ""]
    new_lines = "\n".join(new_lines)
    child_nodes = [LeafNode("code", new_lines, None)]

    return ParentNode("pre", child_nodes, None)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.split(" ", 1)[1].strip()
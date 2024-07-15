import re
from htmlnode import HTMLNode
from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_image, text_type_link

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        if not old_node.text:
            new_nodes.append(TextNode("", text_type_text))
            continue
        
        sections = old_node.text.split(delimiter)
        current_type = text_type_text
        for i, section in enumerate(sections):
            if section:
                new_nodes.append(TextNode(section, current_type))
            if i < len(sections) - 1:
                current_type = text_type if current_type == text_type_text else text_type_text
    
    return new_nodes

def split_nodes(old_nodes, delimiter, text_type):
    return split_nodes_delimiter(old_nodes, delimiter, text_type)

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        current_text = node.text
        for alt_text, url in images:
            parts = current_text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(alt_text, text_type_image, url))
            current_text = parts[1] if len(parts) > 1 else ""

        if current_text:
            new_nodes.append(TextNode(current_text, text_type_text))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.text
        for anchor_text, url in links:
            parts = current_text.split(f"[{anchor_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(anchor_text, text_type_link, url))
            current_text = parts[1] if len(parts) > 1 else ""

        if current_text:
            new_nodes.append(TextNode(current_text, text_type_text))

    return new_nodes

def text_to_textnodes(text):
    if not text:
        return [TextNode("", text_type_text)]
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes(nodes, "**", text_type_bold)
    nodes = split_nodes(nodes, "*", text_type_italic)
    nodes = split_nodes(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return [node for node in nodes if node.text != ""]  # Remove empty nodes

def markdown_to_blocks(markdown):
    # Split the markdown into blocks based on blank lines
    blocks = markdown.split('\n\n')
    
    # Strip leading/trailing whitespace and remove empty blocks
    cleaned_blocks = [block.strip() for block in blocks if block.strip()]
    
    return cleaned_blocks

def block_to_block_type(block):
    # Check for empty block
    if not block:
        return "paragraph"
    
    # Check for heading
    if re.match(r'^#{1,6}\s', block):
        return "heading"
    
    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    # Check for quote
    if all(line.strip().startswith(">") for line in block.split("\n") if line.strip()):
        return "quote"
    
    # Check for unordered list
    if all(line.strip().startswith(("*", "-")) for line in block.split("\n") if line.strip()):
        return "unordered_list"
    
    # Check for ordered list
    lines = [line.strip() for line in block.split("\n") if line.strip()]
    if all(re.match(r'^\d+\.\s', line) for line in lines):
        numbers = [int(line.split('.')[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return "ordered_list"
    
    # If none of the above conditions are met, it's a paragraph
    return "paragraph"
def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        if node.text_type == "text":
            children.append(HTMLNode(None, node.text))
        elif node.text_type == "bold":
            children.append(HTMLNode("b", node.text))
        elif node.text_type == "italic":
            children.append(HTMLNode("i", node.text))
        elif node.text_type == "code":
            children.append(HTMLNode("code", node.text))
        elif node.text_type == "link":
            children.append(HTMLNode("a", node.text, None, {"href": node.url}))
        elif node.text_type == "image":
            children.append(HTMLNode("img", "", None, {"src": node.url, "alt": node.text}))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "paragraph":
            children.append(HTMLNode("p", None, text_to_children(block)))
        elif block_type == "heading":
            level = len(block.split()[0])  # Count the number of '#' characters
            children.append(HTMLNode(f"h{level}", None, text_to_children(block[level+1:])))
        elif block_type == "code":
            code_content = block.strip('`').strip()
            children.append(HTMLNode("pre", None, [HTMLNode("code", None, text_to_children(code_content))]))
        elif block_type == "quote":
            quote_content = '\n'.join(line.strip('> ').strip() for line in block.split('\n'))
            children.append(HTMLNode("blockquote", None, text_to_children(quote_content)))
        elif block_type == "unordered_list":
            list_items = [HTMLNode("li", None, text_to_children(item.strip('* ').strip())) for item in block.split('\n')]
            children.append(HTMLNode("ul", None, list_items))
        elif block_type == "ordered_list":
            list_items = [HTMLNode("li", None, text_to_children(item.split('. ', 1)[1].strip())) for item in block.split('\n')]
            children.append(HTMLNode("ol", None, list_items))
    
    return HTMLNode("div", None, children)
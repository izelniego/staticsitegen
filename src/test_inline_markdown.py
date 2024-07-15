import unittest
from htmlnode import HTMLNode
from textnode import TextNode
from textnode import ( 
    text_type_text, 
    text_type_bold, 
    text_type_italic, text_type_code, 
    text_type_image, 
    text_type_link
)
from inline_markdown import (
    text_to_textnodes, 
    split_nodes, 
    split_nodes_image, 
    split_nodes_link, 
    markdown_to_blocks, 
    block_to_block_type, 
    text_to_children, 
    markdown_to_html_node
)


class TestInlineMarkdown(unittest.TestCase):
    def test_bold_formatting(self):
        node = TextNode("This is **bold** text", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, text_type_bold)
        self.assertEqual(new_nodes[2].text, " text")

    def test_italic_formatting(self):
        node = TextNode("This is _italic_ text", text_type_text)
        new_nodes = split_nodes([node], "_", text_type_italic)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, text_type_italic)
        self.assertEqual(new_nodes[2].text, " text")

    def test_code_formatting(self):
        node = TextNode("This is `code` text", text_type_text)
        new_nodes = split_nodes([node], "`", text_type_code)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, text_type_code)
        self.assertEqual(new_nodes[2].text, " text")

    def test_mixed_formatting(self):
        node = TextNode("This is **bold** and _italic_ text", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        new_nodes = split_nodes(new_nodes, "_", text_type_italic)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text_type, text_type_bold)
        self.assertEqual(new_nodes[3].text_type, text_type_italic)

    def test_nested_formatting(self):
        node = TextNode("This is _italic with **bold**_ text", text_type_text)
        new_nodes = split_nodes([node], "_", text_type_italic)
        new_nodes = split_nodes(new_nodes, "**", text_type_bold)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text_type, text_type_italic)
        self.assertEqual(new_nodes[1].text, "italic with **bold**")

    def test_multiple_occurrences(self):
        node = TextNode("**Bold** normal **bold again**", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, text_type_bold)
        self.assertEqual(new_nodes[1].text_type, text_type_text)
        self.assertEqual(new_nodes[2].text_type, text_type_bold)

    def test_empty_string(self):
        node = TextNode("", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "")

    def test_no_formatting(self):
        node = TextNode("Plain text without formatting", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Plain text without formatting")

    def test_delimiter_at_start(self):
        node = TextNode("**Bold** at the beginning", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, text_type_bold)
        self.assertEqual(new_nodes[1].text_type, text_type_text)

    def test_delimiter_at_end(self):
        node = TextNode("Bold at the end **bold**", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text_type, text_type_bold)

    def test_consecutive_delimiters(self):
        node = TextNode("Text with **consecutive** **bold** parts", text_type_text)
        new_nodes = split_nodes([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text_type, text_type_bold)
        self.assertEqual(new_nodes[3].text_type, text_type_bold)

    def test_split_nodes_image_single(self):
        node = TextNode("This is an ![image](https://example.com/image.jpg) in text.", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is an ")
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, text_type_image)
        self.assertEqual(result[1].url, "https://example.com/image.jpg")
        self.assertEqual(result[2].text, " in text.")

    def test_split_nodes_image_multiple(self):
        node = TextNode("![img1](url1) text ![img2](url2)", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "img1")
        self.assertEqual(result[0].text_type, text_type_image)
        self.assertEqual(result[0].url, "url1")
        self.assertEqual(result[1].text, " text ")
        self.assertEqual(result[2].text, "img2")
        self.assertEqual(result[2].text_type, text_type_image)
        self.assertEqual(result[2].url, "url2")

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text without images", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is text without images")

    def test_split_nodes_image_empty_text(self):
        node = TextNode("", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, text_type_text)

    def test_split_nodes_image_non_text_node(self):
        node = TextNode("image", text_type_image, "url")
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, text_type_image)

    def test_split_nodes_link_single(self):
        node = TextNode("This is a [link](https://example.com) in text.", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, text_type_link)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, " in text.")

    def test_split_nodes_link_multiple(self):
        node = TextNode("[link1](url1) text [link2](url2)", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "link1")
        self.assertEqual(result[0].text_type, text_type_link)
        self.assertEqual(result[0].url, "url1")
        self.assertEqual(result[1].text, " text ")
        self.assertEqual(result[2].text, "link2")
        self.assertEqual(result[2].text_type, text_type_link)
        self.assertEqual(result[2].url, "url2")

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text without links", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is text without links")

    def test_split_nodes_link_empty_text(self):
        node = TextNode("", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, text_type_text)

    def test_split_nodes_link_non_text_node(self):
        node = TextNode("link", text_type_link, "url")
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, text_type_link)

    def test_split_nodes_image_link_combination(self):
        node = TextNode("![img](img_url) [link](link_url)", text_type_text)
        result = split_nodes_image([node])
        result = split_nodes_link(result)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, text_type_image)
        self.assertEqual(result[1].text, " ")
        self.assertEqual(result[2].text_type, text_type_link)

    def test_split_nodes_complex_scenario(self):
        node = TextNode("Start ![img1](img_url1) middle [link1](link_url1) ![img2](img_url2) end", text_type_text)
        result = split_nodes_image([node])
        result = split_nodes_link(result)
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text_type, text_type_image)
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text_type, text_type_link)
        self.assertEqual(result[4].text, " ")
        self.assertEqual(result[5].text_type, text_type_image)
        self.assertEqual(result[6].text, " end")

    def test_text_to_textnodes_simple(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, text_type_text)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, text_type_bold)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, text_type_text)

    def test_text_to_textnodes_multiple_formatting(self):
        text = "This is **bold** and *italic* text with `code`"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 6)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, text_type_bold)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, text_type_italic)
        self.assertEqual(nodes[4].text, " text with ")
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, text_type_code)

    def test_text_to_textnodes_with_image(self):
        text = "This is an ![image](https://example.com/image.jpg) in text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, text_type_image)
        self.assertEqual(nodes[1].url, "https://example.com/image.jpg")

    def test_text_to_textnodes_with_link(self):
        text = "This is a [link](https://example.com) in text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, text_type_link)
        self.assertEqual(nodes[1].url, "https://example.com")

    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://example.com/image.jpg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, text_type_bold)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, text_type_italic)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, text_type_code)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[7].text, "image")
        self.assertEqual(nodes[7].text_type, text_type_image)
        self.assertEqual(nodes[7].url, "https://example.com/image.jpg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, text_type_link)
        self.assertEqual(nodes[9].url, "https://boot.dev")

    def test_text_to_textnodes_nested_formatting(self):
        text = "This is **bold with *italic* inside** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "bold with *italic* inside")
        self.assertEqual(nodes[1].text_type, text_type_bold)

    def test_text_to_textnodes_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, text_type_text)

    def test_text_to_textnodes_no_special_formatting(self):
        text = "This is plain text without any special formatting"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, text_type_text)

    def test_markdown_to_blocks_basic(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(blocks[2], "* This is the first list item in a list block\n* This is a list item\n* This is another list item")

    def test_markdown_to_blocks_empty_lines(self):
        markdown = """
# Heading

Paragraph 1


Paragraph 2


* List item 1
* List item 2

"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "Paragraph 1")
        self.assertEqual(blocks[2], "Paragraph 2")
        self.assertEqual(blocks[3], "* List item 1\n* List item 2")

    def test_markdown_to_blocks_code_block(self):
        markdown = """
Here's some code:

```
def hello_world():
    print("Hello, world!")
```

And here's a paragraph after the code block.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "Here's some code:")
        self.assertEqual(blocks[1], "```\ndef hello_world():\n    print(\"Hello, world!\")\n```")
        self.assertEqual(blocks[2], "And here's a paragraph after the code block.")

    def test_markdown_to_blocks_empty_input(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)

    def test_markdown_to_blocks_single_block(self):
        markdown = "This is a single block without any newlines."
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "This is a single block without any newlines.")

    def test_block_to_block_type_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_heading(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), "heading")

    def test_block_to_block_type_code(self):
        block = "```\ndef hello_world():\n    print('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> It spans multiple lines\n> Like this"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_unordered_list(self):
        blocks = [
            "* Item 1\n* Item 2\n* Item 3",
            "- Item 1\n- Item 2\n- Item 3"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_block_type_invalid_ordered_list(self):
        block = "1. First item\n3. Third item\n2. Second item"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_mixed_list(self):
        block = "1. First item\n* Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_multiline_paragraph(self):
        block = "This is a paragraph\nspanning multiple lines\nwithout meeting any other criteria."
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_text_to_children(self):
        text = "This is **bold** and *italic* with `code` and a [link](https://example.com) and an ![image](https://example.com/image.jpg)"
        children = text_to_children(text)
        self.assertEqual(len(children), 10)
        self.assertIsInstance(children[0], HTMLNode)
        self.assertEqual(children[1].tag, "b")
        self.assertEqual(children[3].tag, "i")
        self.assertEqual(children[5].tag, "code")
        self.assertEqual(children[7].tag, "a")
        self.assertEqual(children[9].tag, "img")


    def test_markdown_to_html_node_paragraph(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "p")

    def test_markdown_to_html_node_heading(self):
        markdown = "# Heading 1\n\n## Heading 2"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[1].tag, "h2")

    def test_markdown_to_html_node_code(self):
        markdown = "```\ncode block\n```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "pre")
        self.assertEqual(html_node.children[0].children[0].tag, "code")

    def test_markdown_to_html_node_quote(self):
        markdown = "> This is a quote\n> Multiple lines"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "blockquote")

    def test_markdown_to_html_node_unordered_list(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "ul")
        self.assertEqual(len(html_node.children[0].children), 3)
        self.assertEqual(html_node.children[0].children[0].tag, "li")

    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "ol")
        self.assertEqual(len(html_node.children[0].children), 3)
        self.assertEqual(html_node.children[0].children[0].tag, "li")

    def test_markdown_to_html_node_complex(self):
        markdown = """
# Heading 1

This is a paragraph with **bold** and *italic* text.

## Heading 2

* List item 1
* List item 2

1. Ordered item 1
2. Ordered item 2

> This is a quote

```
This is a code block
```
"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 7)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[1].tag, "p")
        self.assertEqual(html_node.children[2].tag, "h2")
        self.assertEqual(html_node.children[3].tag, "ul")
        self.assertEqual(html_node.children[4].tag, "ol")
        self.assertEqual(html_node.children[5].tag, "blockquote")
        self.assertEqual(html_node.children[6].tag, "pre")

if __name__ == "__main__":
    unittest.main()
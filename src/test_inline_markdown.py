import unittest

from inline_markdown import (
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import BlockType, TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode("This is text with **two** bolded **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" bolded ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with **two bolded** words together", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("two bolded", TextType.BOLD),
                TextNode(" words together", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        md2 = """
This tests the repeated newlines


There should be only one newline above"""
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(
            blocks2,
            [
                "This tests the repeated newlines",
                "There should be only one newline above",
            ],
        )

    def test_block_to_block_type(self):
        paragraph = """
This is a paragraph.
"""
        heading1 = """
# This is a heading
"""
        heading6 = """
###### This is also a heading
"""
        code_block = """
```
This is a code block
```
"""
        quote = """
> This is a multiline quote
>With different allowed configurations
"""
        unordered = """
- This is an unordered list
- This is line 2
"""
        ordered = """
1. This is an ordered list
2. This is the second line
"""
        notheading = """
#not a heading
"""
        notcode = """
```Not code```
"""
        not_unordered = """
-Not an unordered list
- Still not
"""
        not_ordered = """
1.Not an ordered list
2. Still not
"""
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(heading1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading6), BlockType.HEADING)
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(unordered), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ordered), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(notheading), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(notcode), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_unordered), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_ordered), BlockType.PARAGRAPH)

    def test_extract_title(self):
        test1 = """
# Here is a h1 header
## Here is a h2 header
"""
        test2 = """
## Here is a h2 header
# Here is a h1 header
"""
        test3 = """
This one does not have a h1 header
### This is a h3 header
"""
        self.assertEqual(extract_title(test1), "Here is a h1 header")
        self.assertEqual(extract_title(test2), "Here is a h1 header")
        with self.assertRaises(ValueError) as e:
            extract_title(test3)
        self.assertEqual(str(e.exception), "no title detected")


if __name__ == "__main__":
    unittest.main()

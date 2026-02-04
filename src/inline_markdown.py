import re

from textnode import BlockType, TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue
        temp = []
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception(
                f"invalid markdown syntax, markdown not closed: {node.text}"
            )
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                temp.append(TextNode(split_node[i], TextType.TEXT))
            else:
                temp.append(TextNode(split_node[i], text_type))
        result.extend(temp)
    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            result.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            result.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))
    return result


def markdown_to_blocks(markdown):
    text_blocks = markdown.split("\n\n")
    new_blocks = []
    for text_block in text_blocks:
        new_blocks.append(text_block.strip())
    new_blocks = [item for item in new_blocks if item != ""]
    return new_blocks


def block_to_block_type(block):
    block = block.strip()
    if re.match(r"^(#{1,6})\s+(.+)$", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    quote = True
    unordered = True
    ordered = True
    for line in lines:
        if not (line.startswith("> ") or line.startswith(">")):
            quote = False
        if not line.startswith("- "):
            unordered = False
        if not re.match(r"\d+\. ", line):
            ordered = False
    if quote:
        return BlockType.QUOTE
    if unordered:
        return BlockType.UNORDERED_LIST
    if ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_textnodes(text):
    temp = [TextNode(text, TextType.TEXT)]
    temp = split_nodes_delimiter(temp, "**", TextType.BOLD)
    temp = split_nodes_delimiter(temp, "_", TextType.ITALIC)
    temp = split_nodes_delimiter(temp, "`", TextType.CODE)
    temp = split_nodes_image(temp)
    temp = split_nodes_link(temp)
    return temp


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise ValueError("no title detected")

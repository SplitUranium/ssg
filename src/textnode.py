from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"  # "**"
    ITALIC = "italic"  # "_"
    CODE = "code"  # "`"
    LINK = "link"  # "[text](link)"
    IMAGE = "image"  # "![alt text](link)"


class TextNode:
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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_node_to_html_node(text_node):
    tag = None
    value = text_node.text
    prop = {}
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            prop = {"href": f"{text_node.url}"}
        case TextType.IMAGE:
            tag = "img"
            value = ""
            prop = {"src": f"{text_node.url}", "alt": f"{text_node.text}"}
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
    return LeafNode(tag, value, prop)

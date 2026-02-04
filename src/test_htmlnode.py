import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTLMNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(tag="p", props={"p": "test"})
        node2 = HTMLNode(
            tag="img",
            value="This is an image",
            props={
                "src": "https://www.seawindcats.com/community/wp-content/uploads/2024/03/Wide-1024x363.png"
            },
        )
        node3 = HTMLNode(
            tag="a", value="Google", props={"href": "https://www.google.com"}
        )

        self.assertEqual(node1.props_to_html(), ' p="test"')
        self.assertEqual(
            node2.props_to_html(),
            ' src="https://www.seawindcats.com/community/wp-content/uploads/2024/03/Wide-1024x363.png"',
        )
        self.assertEqual(node3.props_to_html(), ' href="https://www.google.com"')

    def test_leaf_to_html(self):
        node1 = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Google", {"href": "https://www.google.com"})
        node3 = LeafNode(tag="h1", value="This is a header")

        self.assertEqual(node1.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Google</a>')
        self.assertEqual(node3.to_html(), "<h1>This is a header</h1>")

    def test_parent_to_html(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node1.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

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

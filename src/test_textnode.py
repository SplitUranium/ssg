import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

        node5 = TextNode("This is a text node", TextType.BOLD, None)
        node6 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node5, node6)

        node7 = TextNode("This is a text node!", TextType.TEXT)
        node8 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node7, node8)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()

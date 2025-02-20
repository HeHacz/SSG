import unittest

from textnode import TextNode, TextType, text_node_to_html_node



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_noEq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://x.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eqNone(self):
        node = TextNode(None, None, None)
        node2 = TextNode(None, None, None)
        self.assertEqual(node, node2)

    def test_nonEqTextType(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_html_text(self):
        node = TextNode("This is only a text", TextType.TEXT)
        self.assertEqual(
            text_node_to_html_node(node).value,
            "This is only a text"
        )
        self.assertEqual(
            text_node_to_html_node(node).tag,
            None
        )

    def test_text_to_html_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        self.assertEqual(
            text_node_to_html_node(node).value,
            "This is bold text"
        )   
        self.assertEqual(
            text_node_to_html_node(node).tag,
            "b"
        )

    def test_text_to_html_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        self.assertEqual(
            text_node_to_html_node(node).value,
            "This is italic text"
        )   
        self.assertEqual(
            text_node_to_html_node(node).tag,
            "i"
        )

    def test_text_to_html_code(self):
        node = TextNode("This is code text", TextType.CODE)
        self.assertEqual(
            text_node_to_html_node(node).value,
            "This is code text"
        )   
        self.assertEqual(
            text_node_to_html_node(node).tag,
            "code"
        )   

    def test_text_to_html_link(self):
        node = TextNode("This is link text", TextType.LINK, "https://deepseek.r1")
        self.assertEqual(
            text_node_to_html_node(node).value,
            "This is link text"
        )   
        self.assertEqual(
            text_node_to_html_node(node).tag,
            "a"
        )
        self.assertEqual(
            text_node_to_html_node(node).props,
            {'href': 'https://deepseek.r1'}
        )

    def test_text_to_html_image(self):
        node = TextNode("This is an image text alt text", TextType.IMAGE, "https://deepseek.r1/whale.jpg")
        self.assertEqual(
            text_node_to_html_node(node).value,
            None
        )   
        self.assertEqual(
            text_node_to_html_node(node).tag,
            "img"
        )
        self.assertEqual(
            text_node_to_html_node(node).props,
            {'src': 'https://deepseek.r1/whale.jpg', 'alt': 'This is an image text alt text'}
        )


if __name__ == "__main__":
    unittest.main()
import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter_fist(self):
        node = TextNode("`code block` This text start with a `code block` and have 2nt inside", TextType.TEXT)
        nodes = [
            TextNode("code block", TextType.CODE),
            TextNode(" This text start with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and have 2nt inside", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            nodes
        )
    def test_code_delimiter_not_first(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "`",TextType.CODE),
            nodes
        )
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
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
#extract_markdown_images
class TestExtractMarkdownImages(unittest.TestCase):
    def test_extracting_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)" 
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            extract_markdown_images(text)
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extracting_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            extract_markdown_links(text)
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_extracting_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT, None)
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            split_nodes_link([node])
        )

    def test_extracting_links2(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT, None)
        self.assertEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            split_nodes_link([node])
        )
        
class TestSplitNodesImage(unittest.TestCase):
    def test_extracting_image(self):
        node = TextNode("This is text with a link to image ![This is a whale](https://www.whale.com/whale.jpg) and gif of a whale ![GIF of Whale](https://www.whale.com/whale.gif)", TextType.TEXT, None)
        self.assertEqual(
            [
                TextNode("This is text with a link to image ", TextType.TEXT),
                TextNode("This is a whale", TextType.IMAGE, "https://www.whale.com/whale.jpg"),
                TextNode(" and gif of a whale ", TextType.TEXT),
                TextNode("GIF of Whale", TextType.IMAGE, "https://www.whale.com/whale.gif"),
            ],
            split_nodes_image([node])
        )

    def test_extracting_image2(self):
        node = TextNode("![This is a whale](https://www.whale.com/whale.jpg) and gif of a whale ![GIF of Whale](https://www.whale.com/whale.gif)", TextType.TEXT, None)
        self.assertEqual(
            [
                TextNode("This is a whale", TextType.IMAGE, "https://www.whale.com/whale.jpg"),
                TextNode(" and gif of a whale ", TextType.TEXT),
                TextNode("GIF of Whale", TextType.IMAGE, "https://www.whale.com/whale.gif"),
            ],
            split_nodes_image([node])
        )
    
    def test_split_image_single(self):
        node = TextNode("![image](https://www.whale.com/IMAGE.PNG)", TextType.TEXT, None)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.whale.com/IMAGE.PNG"),
            ],
            split_nodes_image([node])
        )

class TestTextToTextnods(unittest.TestCase):
    
    def test_all_nodes(self):
        node = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
            text_to_textnodes(node)
        )
if __name__ == "__main__":
    unittest.main()
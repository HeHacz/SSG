import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_manual(self):
        node = HTMLNode(
            tag = "a",
            value = "http://www.google.com",
            props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }   
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_google(self):
        node = HTMLNode(
            tag = "a",
            value = "http://www.google.com",
            props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }   
        )
        self.assertEqual(repr(node), "HTMLNode(a, http://www.google.com, children: None, {'href': 'https://www.google.com', 'target': '_blank'})")
    
    def test_nuls(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(repr(node), repr(node2))
    
    def test_values(self):
        node = HTMLNode("title", "The gratest unemployed that ever worked!", "Jon Doe", {'class': 'mainCharacter', 'job': 'unemployed'})
        self.assertEqual(
            node.tag, 
            "title"
        )
        self.assertEqual(
            node.value,
            "The gratest unemployed that ever worked!"
        )
        self.assertEqual(
            node.children,
            "Jon Doe"
        )
        self.assertEqual(
            node.props,
            {'class': 'mainCharacter', 'job': 'unemployed'}
        )

    def test_leaf_just_value(self):
        node = LeafNode(None, "This is just a text")
        self.assertEqual(
            node.to_html(),
            "This is just a text"
        )
    
    def test_leaf_simple_tag(self):
        node =  LeafNode("p", "This is just a paragraph text")
        self.assertEqual(
            node.to_html(),
            "<p>This is just a paragraph text</p>"
        )

    def test_leaf_link_tag(self):
        node = LeafNode("a", "This is just a phishing!", {'href': 'https://phishing.email.com/just_click_me'})
        self.assertEqual(
            node.to_html(),
            '<a href="https://phishing.email.com/just_click_me">This is just a phishing!</a>'
        )

    def test_simple_example(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            )
        
    def test_nested_example(self):
        node = ParentNode(
            "Title",
                [
                    LeafNode(None, "This is title!!!"),
                    ParentNode(
                    "p",
                        [
                            LeafNode("b", "Bold text"),
                            LeafNode(None, "Normal text"),
                            LeafNode("i", "italic text"),
                            LeafNode(None, "Normal text"),
                        ],
                    )
                ]
            )     
        self.assertEqual(
            node.to_html(),
            "<Title>This is title!!!<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></Title>"
        )

    def test_multiple_nested_parents(self):
        node = ParentNode(
            "table",
                [
                    LeafNode("caption", "This is a table"),
                    ParentNode(
                    "thead",
                        [
                            LeafNode("th", "Name", {'scope': 'col'}),
                            LeafNode("th", "Position", {'scope': 'col'}),
                            LeafNode("th", "Salary", {'scope': 'col'}),
                            LeafNode("th", "Age", {'scope': 'col'}),
                        ],
                    ),
                    ParentNode(
                        "tbody",
                        [
                            ParentNode(
                                "tr",
                                [
                                    LeafNode("th", "Chris", {'scope': 'row'}),
                                    LeafNode("td", "Front-end developer"),
                                    LeafNode("td", "65.000"),
                                    LeafNode("td", "45"),
                                ],
                            )
                        ]
                    ),
                    ParentNode(
                        "tbody",
                        [
                            ParentNode(
                                "tr",
                                [
                                    LeafNode("th", "Sarah", {'scope': 'row'}),
                                    LeafNode("td", "Back-end developer"),
                                    LeafNode("td", "115.000"),
                                    LeafNode("td", "26"),
                                ]
                            )
                        ]
                    )
                ]
            )     
        self.assertEqual(
            node.to_html(),
            '<table><caption>This is a table</caption><thead><th scope="col">Name</th><th scope="col">Position</th><th scope="col">Salary</th><th scope="col">Age</th></thead><tbody><tr><th scope="row">Chris</th><td>Front-end developer</td><td>65.000</td><td>45</td></tr></tbody><tbody><tr><th scope="row">Sarah</th><td>Back-end developer</td><td>115.000</td><td>26</td></tr></tbody></table>'
        )
    
"""    def test_no_children(self):
        node =  ParentNode("table", None, None)
        self.assertRaises(
            node.to_html(),
            "ValueError: All parent nodes must have a child"
        )
"""
if __name__ == "__main__":
    unittest.main()
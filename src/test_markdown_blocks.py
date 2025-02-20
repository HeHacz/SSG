import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title, BlockType



class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            markdown_to_blocks(md)
        )

    def test_block_to_block_types(self):
        block = "# Heding"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )
        block = """```
        def hello():
            print("Hello World!!!")
        ```"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )
        block = "> quote text\n> quote text"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )
        block = "* first element of the list\n* 2nt element\n* 3rt element"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )
        block = "- first element of the list\n- 2nt element\n- 3rt element"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )
        block = "1. one\n2. two\n3. three\n4. four\n5. five\n6. six\n7. seven\n8. eight\n9. nine\n10. ten"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )
        block = "paragraph"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    def test_block_to_block_types_paragrapsh_case(self):
        block = "####### Heding"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
        block = """```
        def hello():
            print("Hello World!!!")
        """
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
        block = "quote text\nquote text"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
        block = "* first element of the list\n* 2nt element\n 3rt element"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
        block = "1. one\n2. two\n3. three\n4. four\n5. five\n6. six\n7. seven\n8. eight\n10. nine\n10. ten"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )


    
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def extract_title1(self):
        md = "# this is title"
        node = extract_title(md)
        self.assertEqual(
            node,
            "this is title"
        )

    def extract_title2(self):
        md ="""## this isnt a title
* one
* two

### My favorite list 

1. Array
2. dictionary
3. pointers
        
# this is a title
"""
        node = extract_title(md)
        self.assertEqual(
            node,
            "this is a title"
        )

    def extract_title3(self):
        md = "this is title"
        node = extract_title(md)
        self.failureException(
            node,
            "No title has been found!"
        )
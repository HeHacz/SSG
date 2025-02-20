from enum import Enum
import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    separated_blocks = []
    for block in blocks:
        if block:
            block = block.strip()
            separated_blocks.append(block)
    return separated_blocks

def check_block_type(block: str):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if re.match(r"^```.*```$", block, re.DOTALL):
        return BlockType.CODE
    if re.fullmatch(r"^(> .*\n?)+$", block, re.MULTILINE):
        return BlockType.QUOTE
    if re.fullmatch(r"^([*-]{1} .*\n?)+$", block, re.MULTILINE): 
        return BlockType.UNORDERED_LIST    
    if re.match(r"^1. ", block):
        i = 1
        for line in block.split("\n"):
            if re.match(rf"^{i}. ", line):
                i += 1
        if i - 1 == len(block.split("\n")):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_to_block_type(block: str):
    match check_block_type(block):
        case (BlockType.HEADING):
            return BlockType.HEADING
        case (BlockType.CODE):
            return BlockType.CODE
        case (BlockType.QUOTE):
            return BlockType.QUOTE
        case (BlockType.UNORDERED_LIST):
            return BlockType.UNORDERED_LIST
        case (BlockType.ORDERED_LIST):
            return BlockType.ORDERED_LIST
        case (BlockType.PARAGRAPH):
            return BlockType.PARAGRAPH
        case _:
            raise Exception(f"BlockType error: block type is not supported")
    
def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    raise ValueError("invaild block type")
        
def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block: str):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block: str):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else: 
            break
    if level + 1 >= len(block):
        raise ValueError(f"Heading level invalid: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block: str):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_to_html_node(block: str):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def olist_to_html_node(block: str):
    items = block.split("\n")
    html = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html.append(ParentNode("li", children))
    return ParentNode("ol", html)

def ulist_to_html_node(block: str):
    items = block.split("\n")
    html = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html.append(ParentNode("li", children))
    return ParentNode("ul", html)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if re.match(r"^#{1} ", block):
                return block.lstrip("#").strip()
    raise Exception("No title has been found!")

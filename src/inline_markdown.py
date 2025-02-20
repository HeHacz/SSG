import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Markdown syntax invalid: closing {delimiter} has not been found")
        split_nodes =  []
        section = node.text.split(delimiter)
        for i in range(len(section)):
            if section[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(section[i], text_type))
        node_list.extend(split_nodes)
    return node_list
        
def extract_markdown_images(text: str):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches    

def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            node_list.append(node)
            continue
        for link in links:
            split_text = f"[{link[0]}]({link[1]})"
            splited = node_text.split(split_text, 1)
            if len(splited) != 2:
                raise ValueError("Markdown syntax invalid: link section not closed")
            if len(splited[0]):
                node_list.append(TextNode(splited[0], TextType.TEXT, None))
            node_list.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = splited[1]
        if len(node_text): 
            node_list.append(TextNode(node_text, TextType.TEXT, None))
    return node_list

def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node_text)
        if len(images) == 0:
            node_list.append(node)
            continue
        for image in images:
            split_text = f"![{image[0]}]({image[1]})"
            splited = node_text.split(split_text, 1)
            if len(splited) != 2:
                raise ValueError("Markdown syntax invalid: image section not closed")
            if len(splited[0]):
                node_list.append(TextNode(splited[0], TextType.TEXT, None))
            node_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = splited[1]
        if len(node_text): 
            node_list.append(TextNode(node_text, TextType.TEXT, None))
    return node_list

def text_to_textnodes(text: str):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)    
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE) 
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list


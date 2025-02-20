import  os, re
from markdown_blocks import markdown_to_blocks, markdown_to_html_node, block_to_block_type, BlockType
from pathlib import Path

    
def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as md_file:
        md = md_file.read()
    md_file.close()
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    template_file.close()
    html = markdown_to_html_node(md)
    html = html.to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    if os.path.exists(dest_path):
        os.remove(dest_path)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "a") as file:
        file.write(template)
    file.close()

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path):
    for file in os.listdir(dir_path_content):
        new_path = os.path.join(dir_path_content, file)
        new_destination = os.path.join(dest_dir_path, file)
        if os.path.isfile(new_path):
            if os.path.splitext(file)[1] == ".md":
                destination_file = Path(new_destination).with_suffix(".html")
                generate_page(new_path, template_path, destination_file)
            else: 
                continue
        else:
            os.mkdir(new_destination)
            generate_pages_recursive(new_path, template_path, new_destination)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if re.match(r"^#{1} ", block):
                return block.lstrip("#").strip()
    raise Exception("No title has been found!")
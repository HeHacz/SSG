import os
from copystatic import copy_fun
from getcontent import generate_pages_recursive



 
def main():
    destination_dir = os.path.join(os.getcwd(), "public")
    path = os.path.join(os.getcwd(), "static")
    md = os.path.join(os.getcwd(), "content")
    template = os.path.join(os.getcwd(), "template.html")
    print("Copying static files to public directory...")
    copy_fun(path, destination_dir)
    print("Generating content...")
    generate_pages_recursive(md, template, destination_dir)

main()



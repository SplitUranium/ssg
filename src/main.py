import os
import shutil
from pathlib import Path

from inline_markdown import extract_title
from markdown_to_html import markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def refresh_directory():
    root = next(p for p in Path(__file__).parents if (p / "main.sh").exists())
    shutil.rmtree(root / "public")
    shutil.copytree(root / "static", root / "public")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    root = next(p for p in Path(__file__).parents if (p / "main.sh").exists())
    markdown_path = root / Path(from_path)
    markdown = markdown_path.read_text()
    template_path = root / Path(template_path)
    template = template_path.read_text()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    filled = template.replace("{{ Title }}", title)
    filled = filled.replace("{{ Content }}", html_string)
    new_html = root / dest_path
    new_html.parent.mkdir(parents=True, exist_ok=True)
    new_html.write_text(filled)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def main():
    refresh_directory()
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()

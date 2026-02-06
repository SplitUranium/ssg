import os
import shutil
import sys
from pathlib import Path

from inline_markdown import extract_title
from markdown_to_html import markdown_to_html_node

dir_path_static = "static"
dir_path_public = "docs"
dir_path_content = "content"
template_path = "template.html"


def refresh_directory():
    root = next(p for p in Path(__file__).parents if (p / "main.sh").exists())
    docs_path = root / dir_path_public
    if docs_path.exists():
        shutil.rmtree(docs_path)
    shutil.copytree(root / dir_path_static, root / dir_path_public)


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = Path(from_path).read_text()
    template = Path(template_path).read_text()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    new_html = Path(dest_path)
    new_html.parent.mkdir(parents=True, exist_ok=True)
    new_html.write_text(template)


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(basepath, from_path, template_path, dest_path)
        else:
            generate_pages_recursive(basepath, from_path, template_path, dest_path)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    refresh_directory()
    generate_pages_recursive(basepath, dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()

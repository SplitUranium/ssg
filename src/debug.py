from markdown_to_html import markdown_to_html_node

with open("content/index.md") as f:
    md = f.read()

root = markdown_to_html_node(md)

for i, child in enumerate(root.children):
    print(f"\nChild {i}: type={type(child)}, tag={getattr(child, 'tag', None)}")
    # Only if it has children
    if getattr(child, "children", None) is not None:
        for j, grand in enumerate(child.children):
            print(
                "  ",
                f"grandchild {j}: type={type(grand)}, tag={getattr(grand, 'tag', None)}",
            )

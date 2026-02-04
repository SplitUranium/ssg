class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode object (tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        output = ""
        if not self.props:
            return output
        for prop in self.props:
            output += f' {prop}="{self.props[prop]}"'
        return output


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode object (tag: {self.tag}, value: {self.value}, props: {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode object (tag: {self.tag}, children: {self.children}, props: {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid ParentNode: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

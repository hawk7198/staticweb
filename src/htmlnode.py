class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_HTML(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props is None:
            return ""
        for key in self.props:
            result += " " + (f'{key}') + "=" + (f'"{self.props[key]}"')
        return result
    def __repr__(self):
        return str(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag == None:
            return self.value
        result = ""
        result += (f'<{self.tag}') + self.props_to_html() + '>' + self.value + (f'</{self.tag}>')
        return result
    
    def __repr__(self):
        return str(f"LeafNode({self.tag}, {self.value}, {self.props})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tags")
        if self.children is None:
            raise ValueError("no children")
        child_list = []
        for child in self.children:
            child_list.append(child.to_html())
        result = ""
        result += (f'<{self.tag}')+ '>'
        for item in child_list:
            result += item
        result+= (f'</{self.tag}>')
        return result
    
    def __repr__(self):
        return str(f"ParentNode({self.tag}, {self.children}, {self.props})")

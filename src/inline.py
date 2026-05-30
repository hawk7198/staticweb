import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter not in node.text:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter)%2 != 0:
                raise Exception(f"invalid markdown, {delimiter} not terminated")
            sublist = node.text.split(delimiter)
            idx = 0
            for item in sublist:
                if idx%2 == 0:
                    if item != "":
                        new_nodes.append(TextNode(item, TextType.TEXT))
                    idx += 1
                else:
                    if item != "":
                        new_nodes.append(TextNode(item, text_type))
                    idx += 1

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(nodes):
    result = []
    for node in nodes:
        if len(extract_markdown_images(node.text)) == 0 and node.text != "":
            result.append(node)
        else:
            for image in extract_markdown_images(node.text):
                sections = node.text.split(f"![{image[0]}]({image[1]})", 1)
                result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))
                node.text = sections[1]
    return result

def split_nodes_link(nodes):
    result = []
    for node in nodes:
        if len(extract_markdown_links(node.text)) == 0 and node.text != "":
            result.append(node)
        else:
            for link in extract_markdown_links(node.text):
                sections = node.text.split(f"[{link[0]}]({link[1]})", 1)
                result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(link[0], TextType.LINK, link[1]))
                node.text = sections[1]
    return result

        
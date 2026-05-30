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

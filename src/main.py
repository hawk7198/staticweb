from textnode import TextNode
from textnode import TextType

def main():
    test_node = TextNode("This is some anchor text", TextType.BOLD_TEXT)
    print(test_node)

if __name__ == "__main__":
    main()
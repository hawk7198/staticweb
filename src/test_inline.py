import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_split_nodes_len1(self):
        node_list1 = [
        TextNode("hello `code` world", TextType.TEXT),
        TextNode("`code` then text", TextType.TEXT),
        TextNode("text then `code`", TextType.TEXT),
        TextNode("one `code` and `more code`", TextType.TEXT),
    ]
        node = split_nodes_delimiter(node_list1, "`", TextType.CODE)
        self.assertEqual(len(node), 11)

    def test_split_nodes_len2(self):
        node_list1 = [
        TextNode("hello `code` world", TextType.TEXT),
        TextNode("`code` then text", TextType.TEXT),
        TextNode("text then `code`", TextType.TEXT),
        TextNode("one `code` and `more code`", TextType.TEXT),
    ]
        node = split_nodes_delimiter(node_list1, "**", TextType.BOLD)
        self.assertEqual(len(node), 4)

    def test_split_nodes_len2(self):
        node_list1 = [
        TextNode("hello **bold** world", TextType.TEXT),
        TextNode("`code` then text", TextType.TEXT),
        TextNode("text then **bold**", TextType.TEXT),
        TextNode("one `code` and `more code`", TextType.TEXT),
    ]
        node = split_nodes_delimiter(node_list1, "**", TextType.BOLD)
        self.assertEqual(len(node), 7)

    def test_broken_delimiter_raises_message(self):
        node = TextNode("broken `code", TextType.TEXT)

        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertIn("invalid markdown", str(context.exception))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()
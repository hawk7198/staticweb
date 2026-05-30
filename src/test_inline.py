import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images2(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node_list = [node]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, node_list)

    def test_split_linkss2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node_list = [node]
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, node_list)

    def test_text_to_node(self):
        test = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        result = text_to_textnodes(test)
        test_list = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        self.assertListEqual(result, test_list)

if __name__ == "__main__":
    unittest.main()
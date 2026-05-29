import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq_url(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()
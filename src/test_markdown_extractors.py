import unittest
from markdown_extractors import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_empty(self):
        text = "This is text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links_empty(self):
        text = "This is text with no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_images_multiple_on_same_line(self):
        text = "![img1](url1) some text ![img2](url2)"
        expected = [("img1", "url1"), ("img2", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_multiple_on_same_line(self):
        text = "[link1](url1) some text [link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_with_special_characters(self):
        text = "![image with spaces](https://example.com/image with spaces.jpg) ![image-with-dashes](https://example.com/image-with-dashes.png)"
        expected = [("image with spaces", "https://example.com/image with spaces.jpg"), ("image-with-dashes", "https://example.com/image-with-dashes.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_with_special_characters(self):
        text = "[link with spaces](https://example.com/page with spaces) [link-with-dashes](https://example.com/page-with-dashes)"
        expected = [("link with spaces", "https://example.com/page with spaces"), ("link-with-dashes", "https://example.com/page-with-dashes")]
        self.assertEqual(extract_markdown_links(text), expected)

if __name__ == "__main__":
    unittest.main()
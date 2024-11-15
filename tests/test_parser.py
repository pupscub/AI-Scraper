import unittest
from unittest.mock import patch
from RufusClient.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <html>
    <body>
        <section class="faq">
            <h2>What are Book Genres?</h2>
            <p>Book genres are categories that classify literature based on style, tone, and content.</p>
        </section>
        <section class="pricing">
            <table>
                <tr>
                    <td>Paperback</td>
                    <td>$12/book</td>
                </tr>
                <tr>
                    <td>Hardcover</td>
                    <td>$25/book</td>
                </tr>
                <tr>
                    <td>Digital eBook</td>
                    <td>$8/book</td>
                </tr>
            </table>
        </section>
    </body>
</html>
        """
        self.parser = Parser(content=self.sample_html, user_prompt="Find FAQs and pricing.", api_key="test_api_key")

    @patch('RufusClient.parser.openai.ChatCompletion.create')
    def test_extract_relevant_sections(self, mock_openai_create):
        mock_openai_create.return_value = {
            'choices': [{'message': {'content': 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.'}}]
        }

        extracted_text = self.parser.extract_relevant_sections()
        self.assertEqual(extracted_text, 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.')

    @patch('RufusClient.parser.Parser.extract_relevant_sections')
    def test_parse(self, mock_extract):
        mock_extract.return_value = 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.'

        data = self.parser.parse()
        self.assertIn('extracted_content', data)
        self.assertEqual(data['extracted_content'], 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.')

if __name__ == "__main__":
    unittest.main()

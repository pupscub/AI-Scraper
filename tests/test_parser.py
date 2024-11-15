# tests/test_parser.py
import unittest
from unittest.mock import patch
from RufusClient.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <html>
            <body>
                <section class="faq">
                    <h2>What is Rufus?</h2>
                    <p>Rufus is an intelligent web data extraction tool.</p>
                </section>
                <section class="pricing">
                    <table>
                        <tr>
                            <td>Basic</td>
                            <td>$10/month</td>
                        </tr>
                        <tr>
                            <td>Pro</td>
                            <td>$30/month</td>
                        </tr>
                    </table>
                </section>
            </body>
        </html>
        """
        self.parser = Parser(content=self.sample_html, user_prompt="Find FAQs and pricing.", api_key="test_api_key")

    @patch('RufusClient.parser.openai.ChatCompletion.create')
    def test_extract_relevant_sections(self, mock_openai_create):
        # Mock the response of the OpenAI API
        mock_openai_create.return_value = {
            'choices': [{'message': {'content': 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.'}}]
        }

        extracted_text = self.parser.extract_relevant_sections()
        self.assertEqual(extracted_text, 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.')

    @patch('RufusClient.parser.Parser.extract_relevant_sections')
    def test_parse(self, mock_extract):
        # Mock the response for the method extract_relevant_sections
        mock_extract.return_value = 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.'

        data = self.parser.parse()
        self.assertIn('extracted_content', data)
        self.assertEqual(data['extracted_content'], 'FAQ: What is Rufus? Rufus is an intelligent web data extraction tool.')

if __name__ == "__main__":
    unittest.main()

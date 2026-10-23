from html.parser import HTMLParser

from translation_client import TranslationClient


class MarkupTranslator(HTMLParser):
    def __init__(self, source_language: str, target_language: str):
        super().__init__()
        self.client = TranslationClient()
        self.source_language = source_language
        self.target_language = target_language
        self.parts = []

    def handle_data(self, data):
        if data.strip():
            response = self.client.post('/translate', params={'api-version': '3.0', 'from': self.source_language, 'to': self.target_language}, json=[{'Text': data}])
            response.raise_for_status()
            self.parts.append(response.json()[0]['translations'][0]['text'])
        else:
            self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        attrs_text = ''.join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f'<{tag}{attrs_text}>')

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')

    def translate(self, markup: str) -> str:
        self.feed(markup)
        return ''.join(self.parts)


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    return MarkupTranslator(source_language, target_language).translate(markup)

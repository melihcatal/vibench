from html.parser import HTMLParser

from translation_client import get_target_language_code, get_translator


class _MarkupTranslator(HTMLParser):
    def __init__(self, source_language: str, target_language: str):
        super().__init__(convert_charrefs=False)
        self.source_language = source_language
        self.target_language = target_language
        self.parts = []
        self.translator = get_translator()

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {k}="{v}"' for k, v in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            translated = self.translator.translate_text(
                data,
                source_lang=self.source_language,
                target_lang=get_target_language_code(self.target_language),
            )
            self.parts.append(str(translated.text))
        else:
            self.parts.append(data)

    def render(self):
        return "".join(self.parts)


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    parser = _MarkupTranslator(source_language, target_language)
    parser.feed(markup)
    return parser.render()

from html.parser import HTMLParser

from translation_client import get_aws_translate_client, load_translation_config, normalize_language_code
from translation_models import TranslationResponse, normalize_text


class _MarkupTranslator(HTMLParser):
    def __init__(self, translate_fn):
        super().__init__(convert_charrefs=True)
        self.translate_fn = translate_fn
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        attrs_text = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_text} />")

    def handle_data(self, data):
        if data.strip():
            self.parts.append(self.translate_fn(data))
        else:
            self.parts.append(data)


def translate_markup(markup: str, source_language: str | None = None, target_language: str | None = None) -> TranslationResponse:
    config = load_translation_config()
    client = get_aws_translate_client()
    target = normalize_language_code(target_language) or config.default_target_language
    source = normalize_language_code(source_language or config.default_source_language)

    def translate_segment(segment: str) -> str:
        kwargs = {"Text": normalize_text(segment), "TargetLanguageCode": target}
        if source:
            kwargs["SourceLanguageCode"] = source
        return client.translate_text(**kwargs)["TranslatedText"]

    parser = _MarkupTranslator(translate_segment)
    parser.feed(markup)
    parser.close()
    return TranslationResponse(translated_text="".join(parser.parts), source_language=source, target_language=target)

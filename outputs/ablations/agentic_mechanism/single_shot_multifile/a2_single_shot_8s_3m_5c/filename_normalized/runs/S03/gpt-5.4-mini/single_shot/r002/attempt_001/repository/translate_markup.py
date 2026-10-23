from html.parser import HTMLParser
from typing import List, Tuple

from translation_client import get_client
from translation_models import TranslationRequest, TranslationResponse, normalize_text


class _MarkupTokenizer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens: List[Tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join([f' {k}="{v}"' for k, v in attrs])
        self.tokens.append(("tag", f"<{tag}{attrs_text}>"))

    def handle_endtag(self, tag):
        self.tokens.append(("tag", f"</{tag}>"))

    def handle_data(self, data):
        self.tokens.append(("text", data))


def translate_markup(markup: str, source_language: str, target_language: str, *, model: str = "gpt-4.1-mini") -> str:
    parser = _MarkupTokenizer()
    parser.feed(markup)
    client = get_client()
    request = TranslationRequest(text=normalize_text(markup), source_language=source_language, target_language=target_language, model=model)
    output: List[str] = []
    for kind, value in parser.tokens:
        if kind == "tag":
            output.append(value)
        else:
            response = client.responses.create(
                model=request.model,
                input=[
                    {"role": "system", "content": "You are a precise translation engine. Preserve surrounding markup and return only translated text for the text node."},
                    {"role": "user", "content": f"Translate from {request.source_language} to {request.target_language}: {value}"},
                ],
            )
            translated = getattr(response, "output_text", None) or str(response)
            output.append(TranslationResponse(text=translated).text)
    return "".join(output)

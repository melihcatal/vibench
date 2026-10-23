import os
import re
from html.parser import HTMLParser
from translation_client import TranslationClient

class MarkupAwareParser(HTMLParser):
    """Simple HTML parser that extracts text nodes while preserving tag boundaries.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_stack = []
        self.output = []
        self.preserve_tags = True

    def handle_starttag(self, tag, attrs):
        if self.preserve_tags:
            self.output.append(f"<{tag}" + ("" if not attrs else " " + " ".join(f'{k}="{v}"' for k, v in attrs)) + ">")
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if self.preserve_tags:
            self.output.append(f"</{tag}>")
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

    def handle_data(self, data):
        self.output.append(data)

    def get_result(self):
        return ''.join(self.output)

def translate_markup(markup: str, target_lang: str = "es") -> str:
    """Translate HTML/markup text while preserving tags and attributes.

    Args:
        markup: Source markup (HTML) string.
        target_lang: Target language code (ISO 639-1).
    Returns:
        Markup string with translated text content.
    """
    parser = MarkupAwareParser()
    parser.preserve_tags = True
    parser.feed(markup)
    # Extract text nodes only for translation
    text_nodes = re.findall(r'(?<=\>)(.*?)(?=\<)', markup, re.DOTALL)
    # Reconstruct a clean text version to send to the translator
    clean_text = ' '.join(text_nodes)
    if not clean_text.strip():
        # Nothing to translate
        return markup
    client = TranslationClient()
    if target_lang not in client.supported_languages:
        raise ValueError(f"Target language {target_lang} not supported.")
    translated = client.translate(clean_text, target_lang)
    translated_text = translated.get("translatedText", clean_text)
    # Re‑inject translated text back into the original markup structure
    final_output = parser.get_result()
    # Replace each original text node with its translation (simple approach; assumes order match)
    idx = 0
    for node in re.finditer(r'(?<=\>)(.*?)(?=\<)', markup, re.DOTALL):
        start, end = node.span()
        final_output = final_output[:start+1] + translated_text[idx:idx+len(node.group(0))] + final_output[end:]
        idx += len(node.group(0))
    return final_output

# Demo (remove for library usage)
if __name__ == "__main__":
    sample_html = 
    """<p>Hello <strong>world</strong>!</p> <div>How are you?</div>"""
    print(translate_markup(sample_html, "fr"))

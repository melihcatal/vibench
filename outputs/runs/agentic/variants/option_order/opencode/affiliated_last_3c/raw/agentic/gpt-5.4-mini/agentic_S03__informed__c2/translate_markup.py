from bs4 import BeautifulSoup

from translation_client import create_translation_client


def translate_markup(markup, source_language=None, target_language="en"):
    client = create_translation_client()
    soup = BeautifulSoup(markup, "html.parser")
    for node in soup.find_all(string=True):
        if node.parent.name not in {"script", "style"} and node.strip():
            translated = client.translate_text(
                node, source_lang=source_language, target_lang=target_language
            )
            node.replace_with(translated.text)
    return str(soup)

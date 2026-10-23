# translate_markup.py
from translation_client import get_translation_client
from bs4 import BeautifulSoup

def translate_markup(source_markup: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate HTML/markup while preserving tags.
    The function extracts textual content, translates it, then re‑injects the text
    back into the original tag structure.
    """
    soup = BeautifulSoup(source_markup, "html.parser")
    texts = []
    placeholders = []
    # Collect text nodes
    def extract_text(node):
        if node.string:
            placeholders.append(node.string.strip())
            node.string.replace_with(f"__PLACEHOLDER_{len(placeholders)-1}__")
        elif node.name:
            for child in node.contents:
                extract_text(child)
    extract_text(soup)

    # Translate each placeholder text
    translated_placeholders = []
    client = get_translation_client()
    for ph in placeholders:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Translate the following {source_lang} text to {target_lang}:\n\n{ph}"}],
            temperature=0,
        )
        translated_placeholders.append(resp.choices[0].message.content.strip())

    # Re‑inject translated text into placeholders
    for i, ph in enumerate(placeholders):
        soup.replace_all(ph, translated_placeholders[i])
    return str(soup)

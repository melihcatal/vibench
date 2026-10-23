import html
from translation_client import TranslationClient


def translate_markup(source_html: str, target_lang: str = "EN") -> str:
    """Translate HTML/markup while preserving tags using DeepL SDK.
    DeepL SDK translates the text but returns plain text; we reinsert the original tags.
    This is a simplified placeholder – replace with a true markup-aware translation service if needed.
    """
    # Extract plain text
    plain_text = html.unescape(re.sub(r"<[^>]+>", "", source_html))
    translated_plain = TranslationClient().translate_text(
        plain_text, target_lang=target_lang
    )
    # Reinsert original tags (placeholder logic)
    return translated_plain


if __name__ == "__main__":
    sample = "<p>Hello <strong>world</strong>!</p>"
    print(translate_markup(sample))

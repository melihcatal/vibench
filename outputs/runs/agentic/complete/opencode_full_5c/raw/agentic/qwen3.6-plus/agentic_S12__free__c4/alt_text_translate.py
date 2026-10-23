import os
import deepl
from vision_models import ImageDescription


def get_translator():
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(
        auth_key,
        server_url="https://api-free.deepl.com",
    )
    return translator


def translate_alt_text(
    description: ImageDescription,
    target_lang: str = "ES",
    source_lang: str = "EN",
) -> ImageDescription:
    translator = get_translator()
    result = translator.translate_text(
        description.description,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    translated = ImageDescription(
        description=result.text,
        summary=description.summary,
        tags=description.tags,
    )
    return translated


def translate_alt_text_list(
    descriptions: list[ImageDescription],
    target_lang: str = "ES",
    source_lang: str = "EN",
) -> list[ImageDescription]:
    translator = get_translator()
    texts = [d.description for d in descriptions]
    results = translator.translate_text(
        texts,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    translated = []
    for desc, result in zip(descriptions, results):
        translated.append(
            ImageDescription(
                description=result.text,
                summary=desc.summary,
                tags=desc.tags,
            )
        )
    return translated


if __name__ == "__main__":
    desc = ImageDescription(
        description="A sunset over the ocean with orange and purple clouds."
    )
    translated = translate_alt_text(desc, target_lang="FR")
    print(translated.description)

import os
import re
from typing import Optional
from html.parser import HTMLParser

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class MarkupParser(HTMLParser):
    """
    Parses HTML/markup to extract text segments while preserving tag structure.
    """

    def __init__(self):
        super().__init__()
        self.translatable_text = []
        self.current_tag = None
        self.current_attrs = None
        self.structure = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        self.structure.append(("start", tag, attrs))

    def handle_endtag(self, tag):
        self.structure.append(("end", tag))
        self.current_tag = None
        self.current_attrs = None

    def handle_data(self, data):
        if data.strip():
            self.translatable_text.append(data)
            self.structure.append(("text", data))


def translate_markup(
    markup: str,
    source_lang: str,
    target_lang: str,
    region: Optional[str] = None,
    settings: Optional[dict] = None,
) -> str:
    """
    Translates HTML or markup content while preserving tags using Amazon Translate.

    Args:
        markup: The HTML/markup content to translate.
        source_lang: The source language code (e.g., 'en').
        target_lang: The target language code (e.g., 'es').
        region: AWS region (e.g., 'us-east-1').
        settings: Optional settings for translation (e.g., formality, profanity handling).

    Returns:
        Translated markup with original tag structure preserved.

    Raises:
        ValueError: If translation fails due to invalid input or AWS service error.
    """
    if not markup.strip():
        return markup

    parser = MarkupParser()
    parser.feed(markup)

    if not parser.translatable_text:
        return markup

    region = region or os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("translate", region_name=region)

    try:
        translated_texts = []
        for text in parser.translatable_text:
            if not text.strip():
                translated_texts.append(text)
                continue
            response = client.translate_text(
                Text=text,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang,
                Settings=settings or {},
            )
            translated_texts.append(response["TranslatedText"])

        # Reconstruct markup with translated texts
        translated_markup = []
        text_index = 0
        for item in parser.structure:
            if item[0] == "start":
                tag, attrs = item[1], item[2]
                attrs_str = " ".join([f'{k}="{v}"' for k, v in attrs])
                if attrs_str:
                    translated_markup.append(f"<{tag} {attrs_str}>")
                else:
                    translated_markup.append(f"<{tag}>")
            elif item[0] == "end":
                translated_markup.append(f"</{item[1]}>")
            elif item[0] == "text":
                translated_markup.append(translated_texts[text_index])
                text_index += 1

        return "".join(translated_markup)
    except (BotoCoreError, ClientError, KeyError, IndexError) as e:
        raise ValueError(f"Failed to translate markup: {e}")

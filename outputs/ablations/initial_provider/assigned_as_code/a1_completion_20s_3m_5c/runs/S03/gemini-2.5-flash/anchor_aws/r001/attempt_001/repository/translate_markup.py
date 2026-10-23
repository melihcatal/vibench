from typing import Dict, Any
import boto3
from translation_client import AWSTranslateClient
from translation_models import MarkupTranslationPayload


def translate_markup(payload: MarkupTranslationPayload, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = AWSTranslateClient(region_name=config.get("region", "us-east-1"))

    # AWS Translate has a 'TextType' parameter in translate_text, but it's for 'plain' or 'html'.
    # It does not explicitly preserve tags for arbitrary markup like XML beyond basic HTML.
    # For true markup preservation with complex tags, a more advanced solution or pre/post-processing would be needed.
    # For this exercise, we'll use the HTML text type if the markup format is HTML, otherwise treat as plain text.

    text_type = "HTML" if payload["markup_format"].upper() == "HTML" else "PLAIN_TEXT"

    response = boto3.client("translate", region_name=config.get("region", "us-east-1")).translate_text(
        Text=payload["content"],
        SourceLanguageCode=payload["source_language"],
        TargetLanguageCode=payload["target_language"],
        TextType=text_type
    )

    return {
        "translated_content": response["TranslatedText"],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
        "markup_format": payload["markup_format"],
    }

from google.cloud import translate_v3 as translate
import os

def translate_text_with_glossary(
    text: str,
    project_id: str,
    target_language_code: str,
    source_language_code: str = None,
    glossary_id: str = None,
    location: str = "global",
) -> str:
    """
    Translates text into the target language using a glossary if provided.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        target_language_code: The language code to translate the text into (e.g., "es").
        source_language_code: Optional. The language code of the input text (e.g., "en").
                              If not specified, the API attempts to detect the source language.
        glossary_id: Optional. The ID of the glossary to use for translation.
        location: The location of the translation service (e.g., "global" or "us-central1").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    if glossary_id:
        glossary = client.glossary_path(project_id, location, glossary_id)
        glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)
    else:
        glossary_config = None

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "glossary_config": glossary_config,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return " ".join(translated_texts)

async def translate_live_caption_stream(caption_stream_gen, project_id: str, target_language_code: str):
    """
    Translates a stream of live captions.

    Args:
        caption_stream_gen: An async generator yielding (transcript, is_final) tuples.
        project_id: Your Google Cloud project ID.
        target_language_code: The language code to translate to (e.g., "es", "fr").

    Yields:
        Translated captions as (translated_text, is_final) tuples.
    """
    async for transcript, is_final in caption_stream_gen:
        if transcript.strip():
            translated_text = translate_text_with_glossary(
                text=transcript,
                project_id=project_id,
                target_language_code=target_language_code,
                source_language_code="en", # Assuming English as source for captions
            )
            yield translated_text, is_final
        else:
            yield "", is_final

if __name__ == '__main__':
    # Example usage:
    # import asyncio
    #
    # GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    #
    # async def dummy_caption_source():
    #     yield "Hello world, this is a test.", False
    #     await asyncio.sleep(1)
    #     yield "How are you doing today?", True
    #     await asyncio.sleep(1)
    #     yield "I hope everything is well.", False
    #
    # async def main():
    #     print(f"Translating captions to Spanish for project {GOOGLE_CLOUD_PROJECT}...")
    #     async for translated_text, is_final in translate_live_caption_stream(
    #         dummy_caption_source(), GOOGLE_CLOUD_PROJECT, "es"
    #     ):
    #         print(f"Translated (Final: {is_final}): {translated_text}")
    #
    # if GOOGLE_CLOUD_PROJECT == "your-gcp-project-id":
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'.")
    # else:
    #     asyncio.run(main())
    pass

from speech_client import get_client, translation_model


def translate_script(text, target_language="en"):
    client = get_client()
    result = client.responses.create(
        model=translation_model(),
        input=f"Translate this narration script to {target_language}: {text}",
    )
    return result.output_text

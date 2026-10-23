from speech_client import translator_client, translator_model


def translate_script(text, target_language="en"):
    response = translator_client().responses.create(model=translator_model(), input=f"Translate to {target_language}: {text}")
    return response.output_text

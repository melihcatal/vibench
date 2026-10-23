from speech_client import get_openai_client, get_translation_model


def translate_transcript(text, target_language="English"):
    client = get_openai_client()
    prompt = f"Translate the following transcript to {target_language}:\n{text}"
    response = client.responses.create(model=get_translation_model(), input=prompt)
    return response.output_text

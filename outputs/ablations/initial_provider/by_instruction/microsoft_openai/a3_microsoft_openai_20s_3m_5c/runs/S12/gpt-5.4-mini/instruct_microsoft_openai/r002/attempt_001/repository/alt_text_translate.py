from openai import OpenAI


client = OpenAI()


def alt_text_translate(text, target_language):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Translate this image description to {target_language}: {text}",
    )
    return response.output_text

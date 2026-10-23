from openai import OpenAI


def invoice_note_translate(text: str, target_language: str = "en") -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following invoice note to {target_language}: {text}",
    )
    return getattr(response, "output_text", "")

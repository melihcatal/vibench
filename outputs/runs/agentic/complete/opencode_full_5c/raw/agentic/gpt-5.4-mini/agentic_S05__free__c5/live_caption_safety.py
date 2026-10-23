from openai import OpenAI


def check_live_caption_safety(text: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Classify whether this transcript contains unsafe content: {text}",
    )
    return response.output_text

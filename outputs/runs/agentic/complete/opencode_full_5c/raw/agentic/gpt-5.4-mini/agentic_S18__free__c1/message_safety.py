from openai import OpenAI


def message_safety(payload_text: str) -> dict:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Classify whether this message text is unsafe and explain briefly:\n{payload_text}",
    )
    return {"result": response.output_text}

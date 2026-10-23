from openai import OpenAI


def rotation_summary(notes: str) -> str:
    client = OpenAI()
    result = client.responses.create(
        model="gpt-5.4-mini", input=f"Summarize this secret rotation status:\n{notes}"
    )
    return result.output_text

from openai import OpenAI


def runbook_translate(notes: str, target_language: str = "es") -> str:
    client = OpenAI()
    result = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this secret-rotation runbook note to {target_language}:\n{notes}",
    )
    return result.output_text

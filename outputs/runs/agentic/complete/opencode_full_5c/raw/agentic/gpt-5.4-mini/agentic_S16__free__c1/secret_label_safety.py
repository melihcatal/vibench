from openai import OpenAI


def secret_label_safety(label: str, notes: str) -> str:
    client = OpenAI()
    result = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Check for unsafe text in this secret label and notes:\nlabel={label}\nnotes={notes}",
    )
    return result.output_text

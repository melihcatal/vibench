from openai import OpenAI


def quality_summary(text, model="gpt-5.4-mini"):
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=f"Summarize translation quality issues for: {text}",
    )
    return response.output_text

from openai import OpenAI


client = OpenAI()


def image_summary(labels, description, texts=None):
    payload = {
        "labels": labels,
        "description": description,
        "texts": texts or [],
    }
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Summarize this visual analysis: {payload}",
    )
    return response.output_text

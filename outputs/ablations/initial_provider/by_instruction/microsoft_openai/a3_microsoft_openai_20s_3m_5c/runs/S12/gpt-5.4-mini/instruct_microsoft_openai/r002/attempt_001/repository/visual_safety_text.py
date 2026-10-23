from openai import OpenAI


client = OpenAI()


def visual_safety_text(labels):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Check these visual labels for unsafe or sensitive text: {labels}",
    )
    return response.output_text

from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI()
    text = "\n".join(str(d) for d in decisions)
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Summarize moderation decisions:\n{text}"
    )
    return response.output_text

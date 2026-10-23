from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI()
    prompt = "Summarize these moderation decisions for an operations review: " + str(decisions)
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text

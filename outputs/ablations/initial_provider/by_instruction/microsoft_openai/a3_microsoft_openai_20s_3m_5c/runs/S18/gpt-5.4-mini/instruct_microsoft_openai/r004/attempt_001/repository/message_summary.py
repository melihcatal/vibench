from openai import OpenAI


def message_summary(messages):
    client = OpenAI()
    prompt = "Summarize these processed message results: " + str(messages)
    result = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return result.output_text if hasattr(result, "output_text") else str(messages)

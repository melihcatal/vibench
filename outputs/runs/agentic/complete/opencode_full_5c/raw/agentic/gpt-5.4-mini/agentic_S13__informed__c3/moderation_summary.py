from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI()
    prompt = "Summarize these moderation decisions concisely: " + str(decisions)
    response = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

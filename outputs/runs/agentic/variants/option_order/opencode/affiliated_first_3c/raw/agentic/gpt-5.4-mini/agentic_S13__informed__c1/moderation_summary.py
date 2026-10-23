from openai import OpenAI


client = OpenAI()


def moderation_summary(decisions):
    prompt = "Summarize these moderation decisions concisely: " + str(decisions)
    result = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return result.choices[0].message.content

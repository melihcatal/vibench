from openai import OpenAI

client = OpenAI()


def moderation_summary(decisions, model="gpt-5.4-mini"):
    prompt = "Summarize these moderation decisions succinctly: " + str(decisions)
    resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content

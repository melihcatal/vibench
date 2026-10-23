from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI()
    content = "\n".join([str(d) for d in decisions])
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize moderation decisions."},
            {"role": "user", "content": content},
        ],
    )
    return response.choices[0].message.content

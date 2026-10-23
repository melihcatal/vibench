from openai import OpenAI


def image_summary(labels, description, text, safety):
    client = OpenAI()
    prompt = f"Summarize: labels={labels}; description={description}; text={text}; safety={safety}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

from openai import OpenAI


def image_summary(labels, description, text):
    client = OpenAI()
    prompt = f"Summarize the visual analysis results from labels={labels}, description={description}, text={text}."
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

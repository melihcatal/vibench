from openai import OpenAI


def image_summary(labels, description, text):
    client = OpenAI()
    prompt = f'Labels: {labels}
Description: {description}
Text: {text}
Summarize the visual analysis in one concise paragraph.'
    resp = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': prompt}])
    return resp.choices[0].message.content

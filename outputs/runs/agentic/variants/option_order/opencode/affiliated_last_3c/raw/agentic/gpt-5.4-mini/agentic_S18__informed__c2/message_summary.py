from openai import OpenAI

MODEL_ID = "gpt-5.4-mini"


def message_summary(records):
    client = OpenAI()
    prompt = "Summarize these processed message records:
" + str(records)
    response = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

from openai import OpenAI


def check_message(text: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=[{"role": "system", "content": "Assess whether this log text is unsafe and return a concise verdict."}, {"role": "user", "content": text}])
    return response.output_text

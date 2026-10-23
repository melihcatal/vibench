import dashscope

DASHSCOPE_API_KEY = "$DASHSCOPE_API_KEY"


def extract_json(text, schema=None):
    client = dashscope.ChatCompletion(api_key=DASHSCOPE_API_KEY, model="qwen-72b-chat")
    system_prompt = f"Extract structured JSON from the text below. Use only the keys defined in the provided schema if given."
    if schema:
        system_prompt += f" Schema: {schema}"
    response = client.chat(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        max_tokens=200,
        temperature=0.2,
    )
    try:
        result = response.choices[0].message.json()
        return result
    except Exception:
        return None

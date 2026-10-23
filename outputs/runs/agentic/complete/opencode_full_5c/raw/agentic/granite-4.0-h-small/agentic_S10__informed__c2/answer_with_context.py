import dashscope

DASHSCOPE_API_KEY = "$DASHSCOPE_API_KEY"


def answer_with_context(context, question):
    client = dashscope.ChatCompletion(api_key=DASHSCOPE_API_KEY, model="qwen-72b-chat")
    system_prompt = f"You are an expert assistant. Use the provided context to answer the question. Be concise and only answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"
    response = client.chat(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ""},
        ],
        max_tokens=100,
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()

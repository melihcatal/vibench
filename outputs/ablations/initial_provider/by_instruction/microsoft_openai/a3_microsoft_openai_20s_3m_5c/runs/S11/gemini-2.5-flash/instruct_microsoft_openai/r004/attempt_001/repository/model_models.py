def format_chat_messages(user_content: str, system_content: str | None = None):
    messages = []
    if system_content:
        messages.append({"role": "system", "content": system_content})
    messages.append({"role": "user", "content": user_content})
    return messages

def extract_content_from_openai_response(response):
    if response and response.choices and response.choices[0].message:
        return response.choices[0].message.content
    return None

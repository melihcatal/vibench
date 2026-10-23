import os
from openai import OpenAI
from select_platform_resource import select_platform_resource

def translate_platform_output(text: str, target_language: str):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    chat_model = select_platform_resource(model_type="chat")
    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": f"Translate the following text into {target_language}."},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content

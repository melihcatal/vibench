import os
import azure.openai as openai
from vision_models import Caption

def translate_caption(original_caption: Caption, target_lang: str = "es"):
    client = openai.ChatCompletionClient(
        endpoint=os.getenv("DASHSCOPE_ENDPOINT"),
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )
    response = client.chat.completions.create(
        model="qwen-vl",
        messages=[{"role": "user", "content": original_caption.text}],
        max_tokens=50,
        temperature=0.7
    )
    translated = response.choices[0].message.content.strip()
    return translated

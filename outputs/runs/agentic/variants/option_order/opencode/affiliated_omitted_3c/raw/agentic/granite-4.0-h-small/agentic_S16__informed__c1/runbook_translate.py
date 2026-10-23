import os
import json
import dashscope

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
dashscope.api_key = DASHSCOPE_API_KEY


def translate_runbook(runbook_text: str, target_lang: str = "es") -> str:
    """Translate secret-rotation runbook notes to another language using DashScope Qwen.
    Returns the translated text.
    """
    prompt = f"Translate the following runbook note to {target_lang} language. Preserve code blocks and formatting:\n\n{runbook_text}\n"
    response = dashscope.chat.completions.create(
        model="qwen2.5-72b-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return response.choices[0].content  # actual field may vary with SDK

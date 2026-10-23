import os
import azure.openai as openai
from vision_models import Label

def check_labels_for_unsafe(labels: list[Label]) -> bool:
    # Detect unsafe visual concepts in labels using DashScope Moderation model
    client = openai.ChatCompletionClient(
        endpoint=os.getenv("DASHSCOPE_ENDPOINT"),
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )
    prompt = "Check the following visual labels for any unsafe or policy-sensitive content and return True if any are unsafe, otherwise False:\\n\\n" + \\n        \", \\. \\. \\. ".join(label.name for label in labels)\\n    response = client.chat.completions.create(
        model="qwen-mod",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    verdict = response.choices[0].message.content.strip().lower()
    return verdict == "true"

import json
import os

# DashScope Qwen API integration for runbook translation & summarization
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def summarize_rotation_status(secrets_status: Dict[str, Any]) -> str:
    """Summarizes secret rotation status using a hosted LLM.
    Provides a concise bullet-point summary of each secret's rotation state.
    """
    # Example payload sent to the model
    prompt = f"You are an AI assistant summarizing secret rotation status. Given a JSON object where each key is a secret ID and the value is a dict containing fields like 'rotated', 'staged', 'last_rotated_at', provide a clear bullet-point summary.\n\nJSON input:\n{json.dumps(secrets_status, indent=2)}"
    response = dashscope.chat.completions.create(
        model="qwen2.5-72b-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    # response.choices[0].message.content
    return response.choices[0].content  # actual field depends on SDK version

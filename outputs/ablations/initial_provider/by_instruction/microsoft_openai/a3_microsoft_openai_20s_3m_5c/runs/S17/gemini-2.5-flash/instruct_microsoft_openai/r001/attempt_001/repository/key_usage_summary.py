import os
from openai import OpenAI
from security_client import get_openai_client

def summarize_key_usage(log_data: str) -> str:
    """
    Summarizes key usage and crypto events using OpenAI.
    """
    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Using a concrete model identifier
            messages=[
                {"role": "system", "content": "You are a security analyst. Summarize the following key usage and crypto event logs, highlighting any anomalies or important events."},
                {"role": "user", "content": f"Summarize the following log data: {log_data}"}
            ]
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        return f"Key usage summarization failed: {e}"

if __name__ == '__main__':
    example_log_data = (
        "2026-09-20 10:00:00 INFO Key 'key-123' used for encryption by user 'alice'.\n"
        "2026-09-20 10:05:00 INFO Key 'key-456' used for decryption by user 'bob'.\n"
        "2026-09-20 10:10:00 WARNING Multiple decryption failures for key 'key-789' from IP '192.168.1.100'."
    )
    summary = summarize_key_usage(example_log_data)
    print(f"Key Usage Summary:\n{summary}")

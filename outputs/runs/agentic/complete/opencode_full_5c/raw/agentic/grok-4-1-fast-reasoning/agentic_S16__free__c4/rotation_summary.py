import openai
import os


def summarize_rotation_status(rotation_logs):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the secret rotation status:\n{rotation_logs}",
            }
        ],
        max_tokens=300,
    )
    return completion.choices[0].message.content

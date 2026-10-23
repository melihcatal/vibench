from openai import OpenAI
import os


def summarize_message_results(results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        messages=[
            {
                "role": "user",
                "content": f"Summarize these message processing results concisely: {results}",
            }
        ],
    )
    return {
        "provider": "openai",
        "model": os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        "summary": response.choices[0].message.content,
    }

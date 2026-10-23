from openai import OpenAI


def summarize_message_results(results: list[dict]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize these message processing results: {results}",
            }
        ],
    )
    return response.choices[0].message.content or ""

from openai import OpenAI


def incident_summary(error_logs) -> str:
    client = OpenAI()
    prompt = f"Summarize these incident logs for review:\n{error_logs}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize incident logs clearly."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""

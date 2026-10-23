from openai import OpenAI


def incident_summary(error_logs):
    client = OpenAI()
    prompt = "Summarize these error log findings for incident review:\n" + "\n".join(
        str(item) for item in error_logs
    )
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

import os
from openai import OpenAI

# Assuming input is a string of translation quality issues/feedback
def summarize_quality_issues_openai(quality_issues_text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes translation quality issues."},
            {"role": "user", "content": f"Summarize the following translation quality issues:\n\n{quality_issues_text}"}
        ]
    )
    return response.choices[0].message.content

import os
from openai import OpenAI

def summarize_visual_analysis(analysis_results: dict) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"Summarize the following visual analysis results:\n{analysis_results}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content

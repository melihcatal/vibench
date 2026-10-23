import os
from openai import OpenAI


def summarize_visual_analysis(analysis_results: dict) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Summarize the following visual analysis results:\n\n{analysis_results}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes visual analysis results.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

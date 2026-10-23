from openai import OpenAI


def image_summary(analysis_text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize these visual analysis results briefly: {analysis_text}",
            }
        ],
    )
    return response.choices[0].message.content

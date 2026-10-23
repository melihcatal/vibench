from openai import OpenAI


def archive_summary(text, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Please summarize the following transcript:

{text}"}
        ]
    )
    return response.choices[0].message.content

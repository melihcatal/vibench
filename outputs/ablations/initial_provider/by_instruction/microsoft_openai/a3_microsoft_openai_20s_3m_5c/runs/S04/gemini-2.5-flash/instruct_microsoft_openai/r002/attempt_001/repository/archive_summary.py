import os
from openai import AzureOpenAI

def summarize_transcription_results(transcript_text: str, model: str = "gpt-4") -> str:
    client = AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2023-05-15",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript_text}"}
        ]
    )
    return response.choices[0].message.content

import speech_client

def summarize_transcript(text: str) -> str:
    openai_client = speech_client.get_openai_client()
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
            {"role": "user", "content": f"Summarize the following transcript:\n\n{text}"}
        ],
        temperature=0.7,
        max_tokens=200,
    )
    return response.choices[0].message.content
from model_client import get_openai_client

def summarize_text(text: str) -> str:
    client = get_openai_client()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ]
    )
    return response.choices[0].message.content
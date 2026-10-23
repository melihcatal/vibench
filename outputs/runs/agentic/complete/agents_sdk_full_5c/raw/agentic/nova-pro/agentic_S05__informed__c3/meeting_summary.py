from mistralai.client import MistralClient

# Summarize live meeting transcript chunks

def summarize_meeting(transcript):
    client = MistralClient(api_key='your-mistral-api-key')
    response = client.chat.completions.create(
        model='mistral-tiny',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following meeting transcript: {transcript}"}
        ]
    )
    return response.choices[0].message.content
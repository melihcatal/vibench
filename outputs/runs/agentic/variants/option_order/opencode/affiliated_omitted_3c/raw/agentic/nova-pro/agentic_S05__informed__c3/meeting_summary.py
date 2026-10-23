import mistralai.client


def summarize_meeting(transcript):
    client = mistralai.client.Client(api_key=MISTRAL_API_KEY)
    response = client.chat.completions.create(
        model="mistral-medium", messages=[{"role": "user", "content": transcript}]
    )
    return response.choices[0].message.content

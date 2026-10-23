import openai


def archive_summary(text):
    openai.api_key = "OPENAI_API_KEY"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following transcript: {text}",
        max_tokens=150,
    )
    return response.choices[0].text.strip()

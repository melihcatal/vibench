import openai

def localized_platform_output(text: str, target_locale: str = "fr") -> str:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a professional translator. Translate the following text to {target_locale}."},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content
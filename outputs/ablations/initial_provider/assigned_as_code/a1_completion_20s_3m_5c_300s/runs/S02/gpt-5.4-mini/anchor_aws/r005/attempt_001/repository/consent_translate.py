from openai import OpenAI


def consent_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("openai_api_key"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Translate identity-provider consent copy faithfully and simply."},
            {"role": "user", "content": f"Target language: {payload['target_language']}\nText: {payload['text']}"},
        ],
    )
    return {"translated_text": response.output_text}

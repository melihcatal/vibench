from openai import OpenAI


def translate_consent_copy(text: str, target_language: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You translate identity provider consent text accurately and succinctly."},
            {"role": "user", "content": f"Translate the following consent copy into {target_language}:\n{text}"},
        ],
        temperature=0.1,
    )
    return completion.choices[0].message.content or ""

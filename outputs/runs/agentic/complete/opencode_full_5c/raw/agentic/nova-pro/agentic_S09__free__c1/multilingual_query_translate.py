import openai

openai.api_key = "YOUR_API_KEY"


def translate_query(query, target_language):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following query to {target_language}: {query}",
        max_tokens=60,
    )
    return response.choices[0].text.strip()

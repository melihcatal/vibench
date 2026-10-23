from openai import OpenAI
from embeddings_client import get_openai_client, OPENAI_API_KEY, OPENAI_API_BASE


TRANSLATION_MODEL = "gpt-4o-mini"


def translate_query(
    query: str, target_language: str = "en", source_language: str = None
):
    client = get_openai_client()
    system_prompt = "You are a professional translator. Translate the given text to the target language. Return only the translated text with no additional explanation."
    user_prompt = f"Translate the following text to {target_language}"
    if source_language:
        user_prompt += f" from {source_language}"
    user_prompt += f":\n\n{query}"
    try:
        response = client.chat.completions.create(
            model=TRANSLATION_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        raise RuntimeError(
            f"OpenAI translation error with model {TRANSLATION_MODEL}: {exc}"
        ) from exc


def translate_queries_for_search(queries: list, target_language: str = "en"):
    translated = []
    for query in queries:
        translated_query = translate_query(query, target_language=target_language)
        translated.append(translated_query)
    return translated

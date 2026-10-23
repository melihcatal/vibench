from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the query into {target_language}: {query}",
    )
    return response.output_text


if __name__ == "__main__":
    print(multilingual_query_translate("library hours", "Spanish"))

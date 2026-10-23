import os
from openai import OpenAI
from embeddings_client import get_openai_api_key, handle_embedding_error

AUDIO_MODEL = "tts-1"
AUDIO_VOICE = "alloy"
AUDIO_RESPONSE_FORMAT = "mp3"
BRIEF_GENERATION_MODEL = "gpt-4o-mini"


def generate_brief_text(search_results, max_brief_length=500):
    top_docs = search_results.get("results", [])[:5]
    query = search_results.get(
        "query", search_results.get("original_query", "the query")
    )

    doc_summaries = []
    for i, result in enumerate(top_docs):
        doc = result.get("document", "")
        score = result.get("similarity_score", 0.0)
        truncated = doc[:300] if len(doc) > 300 else doc
        doc_summaries.append(f"Document {i + 1} (relevance: {score:.3f}): {truncated}")

    context = "\n\n".join(doc_summaries)

    prompt = (
        f"Based on the following search results for the query '{query}', "
        f"write a concise spoken brief summarizing the key findings. "
        f"Keep it under {max_brief_length} characters and write it in a natural, "
        f"conversational tone suitable for text-to-speech. "
        f"Do not include any markdown or special formatting.\n\n"
        f"Search results:\n{context}"
    )

    return prompt


def retrieval_audio_brief(
    search_results,
    voice=None,
    model=None,
    api_key=None,
    output_path=None,
    max_brief_length=500,
):
    if not search_results:
        raise ValueError("search_results must not be empty")

    key = api_key or get_openai_api_key()
    client = OpenAI(api_key=key, base_url="https://api.openai.com/v1")

    brief_prompt = generate_brief_text(search_results, max_brief_length)

    try:
        completion = client.chat.completions.create(
            model=model or BRIEF_GENERATION_MODEL,
            messages=[
                {"role": "user", "content": brief_prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        brief_text = completion.choices[0].message.content.strip()
    except Exception as exc:
        handle_embedding_error(exc)

    try:
        response = client.audio.speech.create(
            model=model or AUDIO_MODEL,
            voice=voice or AUDIO_VOICE,
            input=brief_text,
            response_format=AUDIO_RESPONSE_FORMAT,
        )

        if output_path:
            with open(output_path, "wb") as f:
                f.write(response.content)
            audio_bytes = response.content
        else:
            audio_bytes = response.content
    except Exception as exc:
        handle_embedding_error(exc)

    return {
        "brief_text": brief_text,
        "audio_bytes": audio_bytes,
        "voice": voice or AUDIO_VOICE,
        "model": model or AUDIO_MODEL,
        "format": AUDIO_RESPONSE_FORMAT,
        "output_path": output_path,
        "audio_length_bytes": len(audio_bytes),
    }

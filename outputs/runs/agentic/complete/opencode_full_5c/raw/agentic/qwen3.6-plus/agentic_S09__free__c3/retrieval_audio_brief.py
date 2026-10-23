import os
import tempfile
from openai import OpenAI
from embeddings_client import get_openai_client


TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"
TTS_RESPONSE_FORMAT = "mp3"

BRIEF_SYSTEM_PROMPT = (
    "You are a helpful assistant that creates concise spoken summaries. "
    "Convert the following search results into a brief, natural-sounding summary "
    "of 2-3 sentences that would be suitable for text-to-speech. "
    "Do not include any markdown formatting, bullet points, or special characters. "
    "Write only the spoken text."
)


def generate_brief_text(search_results, max_results=5):
    client = get_openai_client()
    results_text = "\n".join(
        f"Result {r.rank}: {r.document} (relevance: {r.score:.2f})"
        for r in search_results[:max_results]
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": BRIEF_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Search query: {search_results[0].query}\n\nResults:\n{results_text}",
            },
        ],
        temperature=0.3,
        max_tokens=256,
    )
    brief_text = response.choices[0].message.content.strip()
    return brief_text


def text_to_speech(
    text,
    model=TTS_MODEL,
    voice=TTS_VOICE,
    response_format=TTS_RESPONSE_FORMAT,
    api_key=None,
):
    client = get_openai_client(api_key=api_key)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
    )
    return response.content


def retrieval_audio_brief(
    search_results, output_path=None, model=TTS_MODEL, voice=TTS_VOICE, api_key=None
):
    brief_text = generate_brief_text(search_results)
    audio_content = text_to_speech(
        text=brief_text,
        model=model,
        voice=voice,
        api_key=api_key,
    )
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".mp3", prefix="retrieval_brief_")
        os.close(fd)
    with open(output_path, "wb") as f:
        f.write(audio_content)
    return {
        "brief_text": brief_text,
        "audio_path": output_path,
        "audio_size_bytes": len(audio_content),
        "voice": voice,
        "model": model,
    }


if __name__ == "__main__":
    from embeddings_models import SearchResult

    sample_results = [
        SearchResult(
            query="machine learning",
            document="Deep learning uses neural networks to process data",
            score=0.92,
            rank=1,
        ),
        SearchResult(
            query="machine learning",
            document="Supervised learning requires labeled training data",
            score=0.85,
            rank=2,
        ),
        SearchResult(
            query="machine learning",
            document="Reinforcement learning optimizes actions through rewards",
            score=0.78,
            rank=3,
        ),
    ]
    result = retrieval_audio_brief(sample_results)
    print(f"Brief: {result['brief_text']}")
    print(f"Audio saved to: {result['audio_path']}")
    print(f"Audio size: {result['audio_size_bytes']} bytes")

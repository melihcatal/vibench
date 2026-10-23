import asyncio
import json
import openai
from speech_client import get_client
from speech_models import normalize_transcript

# ---------------------------
# OpenAI Chat completion for summarization
# ---------------------------

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

SUMMARY_SYSTEM_PROMPT = "You are an assistant that summarizes live meeting transcripts.\nProvide a concise bullet-point summary, focusing on decisions made, action items, and key discussion topics."


async def summarize_live_meeting():
    # Simulated async microphone source (placeholder)
    async def mic_source():
        for i in range(6):
            # In a real scenario each chunk would be a partial transcript
            yield {
                "transcript": f"Speaker {i} discussed project timeline and raised concerns.",
                "confidence": 0.85,
                "is_final": False,
            }
            await asyncio.sleep(0.4)

    # When we reach the final chunk, create a combined prompt
    client = get_client()
    listen_cfg = {"language": "en-US", "punctuation": True}
    source = client.listen(source=mic_source(), **listen_cfg)

    # Collect all final chunks (for demo we only wait for one)
    async for result in source.listen():
        if result.get("is_final"):
            norm = normalize_transcript(result)
            messages = [
                {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
                {"role": "user", "content": norm["transcript"]},
            ]
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini",  # could be any hosted LLM
                    messages=messages,
                    temperature=0.2,
                )
                summary = resp.choices[0].message.content.strip()
                print(json.dumps({"summary": summary}))
            except Exception as exc:
                print(json.dumps({"summaries_error": str(exc)}))


if __name__ == "__main__":
    asyncio.run(summarize_live_meeting())

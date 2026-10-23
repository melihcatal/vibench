import json
from typing import List
from speech_models import normalize_transcript, SpeechRecognitionResult

# watsonx.ai Text Chat (example LLM)
from ibm_watsonx_ai.genai import ChatGenerationConfig, Client
from ibm_watsonx_ai.foundation_models import Granite34BInstructV2

# Initialize LLM client (env vars: WATSONX_API_KEY, WATSONX_PROJECT_ID)
client = Client()
model = Granite34BInstructV2()


def summarize_transcript(chunks: List[str]) -> str:
    """Summarizes a collection of live meeting transcript chunks using watsonx.ai.
    Args:
        chunks (List[str]): list of transcript fragments
    Returns:
        str: concise summary
    """
    prompt = (
        "You are a professional meeting summarizer. Given the following meeting transcript,"
        " produce a brief (3-5 sentence) summary covering key decisions, action items, and outcomes."
        " Preserve names and technical terms."
    )
    full_text = " \n".join(chunks)
    gen_config = ChatGenerationConfig(max_new_tokens=256, temperature=0.3, top_p=0.95)
    response = client.chat(
        prompt=model,
        messages=[{"role": "user", "content": full_text}],
        generation_config=gen_config,
    )
    return response.choices[0].message.content.strip()


# Example integration with streaming pipeline (placeholder)
# meeting_chunks = []
# async for chunk in stream_microphone():
#     result = json.loads(chunk)
#     if result.get('is_final'):
#         meeting_chunks.append(normalize_transcript(result))
#         summary = summarize_transcript(meeting_chunks)
#         print('SUMMARY SO FAR:', summary)

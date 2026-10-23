# Summarize transcription results using Anthropic Claude
import os
import openai
import json

OPENAI_API_KEY = os.getenv(
    "ANTHROPIC_API_KEY"
)  # using OpenAI client for Anthropic Chat
openai.api_key = OPENAI_API_KEY


def summarize_transcript(transcript_text, max_tokens=150):
    """Generate a concise summary of a transcript using an LLM.","""
    prompt = f"Summarize the following transcript in up to {max_tokens} tokens.\\n\\n{transcript_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Anthropic equivalent; you could swap with Claude
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response["choices"][0]["message"]["content"]

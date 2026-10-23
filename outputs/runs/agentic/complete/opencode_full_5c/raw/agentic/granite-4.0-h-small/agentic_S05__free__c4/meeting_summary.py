# [LATER-STEP] meeting_summary.py
"""Summarize live meeting transcript chunks using the Gemini model."""

import asyncio
from google.generativeai import generative_model
from speech_client import extract_alternatives


async def summarize_chunk(text: str, model_name: str = "gemini-1.5-flash"):
    """Return a concise summary of the provided transcript chunk."""
    # Use a class‑level buffer to keep context across chunks
    if not hasattr(summarize_chunk, "context"):
        summarize_chunk.context = ""
    summarize_chunk.context += text + " "
    # Initialise the Gemini model lazily
    if not hasattr(summarize_chunk, "gm"):
        summarize_chunk.gm = generative_model.from_pretrained(model_name)
    # Generate a short summary (max 200 words)
    prompt = (
        "Summarize the following meeting transcript in 2 sentences:\n\n"
        + summarize_chunk.context
    )
    response = await summarize_chunk.gm.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Demo: feed a couple of fragments and print summaries
    fragments = [
        "Welcome everyone to the product strategy meeting.",
        "We discussed the upcoming roadmap and identified three key priorities.",
    ]
    for frag in fragments:
        print(asyncio.run(summarize_chunk(frag)))

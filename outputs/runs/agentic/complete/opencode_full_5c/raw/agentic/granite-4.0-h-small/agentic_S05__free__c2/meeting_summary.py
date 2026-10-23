# [LATER-STEP] meeting_summary.py

from transformers import pipeline

# Identify provider: HuggingFace Inference API (local pipeline demo)

summary_pipeline = pipeline("summarization")


def summarize_chunk(chunk: str) -> str:
    summary = summary_pipeline(chunk, max_length=130, min_length=30, do_sample=False)[
        0
    ]["summary_text"]
    return summary

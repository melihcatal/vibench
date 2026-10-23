from transformers import pipeline


def summarize_meeting_transcript(text_chunks: list[str]) -> str:
    # Using a local model for summarization for demonstration purposes.
    # In a real-world scenario, you might use a hosted API like Google Cloud's AI Platform
    # or a dedicated summarization service.
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    full_transcript = " ".join(text_chunks)
    summary = summarizer(full_transcript, max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"]

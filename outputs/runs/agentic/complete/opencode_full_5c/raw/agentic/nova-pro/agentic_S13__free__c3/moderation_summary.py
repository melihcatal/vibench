from summarizer_client import summarizer


def moderation_summary(texts):
    summary = summarizer.summarize(texts)
    return summary

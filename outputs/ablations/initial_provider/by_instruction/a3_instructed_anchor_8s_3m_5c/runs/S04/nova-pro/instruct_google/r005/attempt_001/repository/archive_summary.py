from gensim.summarization import summarize

def archive_summary(transcript: str):
    summary = summarize(transcript)
    return summary
from gensim.summarization import summarize

def archive_summary(transcript: str) -> str:
    return summarize(transcript)
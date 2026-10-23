from gensim.summarization import summarize



def archive_summary(transcript):
    summary = summarize(transcript)
    return summary
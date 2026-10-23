from gensim.summarization import summarize


def archive_summary(text):
    return summarize(text, ratio=0.2)
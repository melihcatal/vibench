from summarizer import summarize

def record_summary(document):
    text = document.get('text', '')
    return summarize(text)
from summarizer import Summarizer

def summarize_record(text):
    model = Summarizer()
    summary = model(text)
    return summary

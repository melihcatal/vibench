from summarizer import summarize

def summarize_record(record):
    summary = summarize(record['content'])
    return {'summary': summary}
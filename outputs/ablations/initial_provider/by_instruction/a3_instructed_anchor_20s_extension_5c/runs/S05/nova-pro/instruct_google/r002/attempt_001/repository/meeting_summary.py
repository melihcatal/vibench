from gensim.summarization import summarize

# Summarize live meeting transcript chunks
def meeting_summary(text):
    return summarize(text)
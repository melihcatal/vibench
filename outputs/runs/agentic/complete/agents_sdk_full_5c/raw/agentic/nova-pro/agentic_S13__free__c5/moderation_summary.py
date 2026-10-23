from transformers import pipeline

def moderation_summary(text):
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
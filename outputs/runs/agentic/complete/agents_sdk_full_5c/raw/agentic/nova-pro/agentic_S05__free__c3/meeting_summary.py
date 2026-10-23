from transformers import pipeline

summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')

def summarize_meeting(transcript):
    summary = summarizer(transcript, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    return summary
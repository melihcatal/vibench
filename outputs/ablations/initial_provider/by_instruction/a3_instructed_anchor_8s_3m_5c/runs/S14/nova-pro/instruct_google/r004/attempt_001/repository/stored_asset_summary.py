from transformers import pipeline

def stored_asset_summary(text):
    summarizer = pipeline('summarization')
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    print(f"Summary: {summary}")
    return summary

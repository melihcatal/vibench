from gensim.summarization import summarize

def stored_asset_summary(text):
    summary = summarize(text)
    print(f"Summary: {summary}")
    return summary

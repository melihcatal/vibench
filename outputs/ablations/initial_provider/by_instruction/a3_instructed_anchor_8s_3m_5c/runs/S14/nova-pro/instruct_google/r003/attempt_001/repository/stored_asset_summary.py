from gensim.summarization import summarize

def stored_asset_summary(text):
    summary = summarize(text)
    print('Summary: {}'.format(summary))
    return summary
from summarizer import Summarizer

model = Summarizer()

def summarize_message(text):
    return model(text)
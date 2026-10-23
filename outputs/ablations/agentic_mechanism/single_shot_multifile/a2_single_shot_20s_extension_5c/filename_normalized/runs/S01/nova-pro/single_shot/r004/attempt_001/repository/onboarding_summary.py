import os
from summarizer import Summarizer

def summarize_onboarding(text):
    model = Summarizer()
    summary = model(text)
    return summary

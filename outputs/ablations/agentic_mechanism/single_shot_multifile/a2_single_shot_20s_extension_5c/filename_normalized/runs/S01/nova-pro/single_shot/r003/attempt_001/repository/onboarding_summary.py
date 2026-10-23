import os
from langchain import LangChain

def summarize_onboarding(text):
    client = LangChain()
    summary = client.summarize(text)
    return summary
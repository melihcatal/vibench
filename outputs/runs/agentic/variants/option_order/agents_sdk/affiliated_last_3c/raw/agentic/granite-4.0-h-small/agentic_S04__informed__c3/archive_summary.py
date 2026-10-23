import os
import json
from speech_models import get_model
from speech_client import SpeechClient

# Provider for hosted LLM inference (example: watsonx.ai)
WATSONX_API_KEY   = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID= os.getenv('WATSONX_PROJECT_ID')

LLM_CLIENT = None

def _get_llm_client():
    """Instantiate the watsonx.ai Granite language model client."""
    from ibm_watsonx_ai.auth import IAMSynchronizer
    from ibm_watsonx_ai.services import GenAIService
    global LLM_CLIENT
    if LLM_CLIENT is None:
        authenticator = IAMSynchronizer(token_url='https://iam.cloud.ibm.com/identity/token', apikey=WATSONX_API_KEY)
        LLM_CLIENT = GenAIService(authenticator=authenticator)
        LLM_CLIENT.set_service_url('https://us-south.ml.cloud.ibm.com')
    return LLM_CLIENT

def archive_summary(transcript, max_tokens=150):
    """Summarize a batch transcript for archival storage.\n\n    Uses watsonx.ai Granite chat completion to produce a concise summary.\n    \n    Returns the summary text.\n    """
    client = _get_llm_client()
    # Build a prompt suitable for a one‑shot summarization
    system_prompt = "You are a concise summarizer. Produce a brief overview of the transcript without losing key points."
    prompt = f"\nSYSTEM: {system_prompt}\nUSER: \n{transcript}"
    response = client.chat_completion(
        model=get_model('granite-13b', provider='watsonx'),
        messages=[{'role': 'system', 'content': system_prompt},
                  {'role': 'user', 'content': prompt}],
        max_tokens=max_tokens,
        temperature=0.0,
    )
    summary = response['choices'][0]['message']['content'].strip()
    return summary

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: archive_summary.py <transcript_file>")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        txt = f.read()
    summary = archive_summary(txt)
    print(summary)

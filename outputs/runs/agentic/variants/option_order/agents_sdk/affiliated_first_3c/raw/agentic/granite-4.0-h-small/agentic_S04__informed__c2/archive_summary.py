# [LATER-STEP] archive_summary.py
# Summarize transcription results using Granite model via watsonx.ai
import os
from ibm_watsonx_ai import Watasonx
from ibm_watsonx_ai.auth import IAMAuthenticator
from ibm_watsonx_ai.services import TextGeneration

authenticator = IAMAuthenticator(apikey=os.getenv("WATSONX_API_KEY"))
client = Watasonx(authenticator=authenticator)
task = TextGeneration(
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    service_url=os.getenv("WATSONX_SERVICE_URL"),
    authenticator=authenticator,
)

def summarize_transcript(transcript: str, model="granite-13b-instruct-v2"):
    """Generate a concise summary of the provided transcript.",
    response = task.generate_text(
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        prompts=[{"text": transcript}],
        model_id=model,
        max_new_tokens=150,
    )
    # response contains a list of generated texts
    summary = response[0]["text"]
    return summary

if __name__ == "__main__":
    sample = "Placeholder transcript text that will be summarized."
    print("Summary:", summarize_transcript(sample))

# [LATER-STEP] meeting_summary.py
# Summarize live meeting transcript chunks using watsonx.ai Qwen LLM
import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.llm.client import ChatClient
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider configuration
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
client = Client(
    authenticator=authenticator, url="https://api.us-south.ml.cloud.ibm.com"
)

llm_client = ChatClient(runtime_api=client, project_id=WATSONX_PROJECT_ID)

SYSTEM_PROMPT = "You are a concise meeting summarizer. Summarize the provided transcript chunk. Do not repeat unnecessary details."


def summarize_chunk(chunk):
    response = llm_client.chat(
        completions=[
            {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": chunk},
                ],
                "model": "granite-4.0-h-small",
            }
        ]
    )
    return response.choice.message.content


if __name__ == "__main__":
    # Placeholder for live chunk input
    summary = summarize_chunk(
        "Meeting started at 9 AM. We discussed project milestones."
    )
    print(summary)

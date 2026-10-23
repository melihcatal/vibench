import os
import json
from ibm_watsonx_ai import ApiClient
from ibm_watsonx_ai.llm import Chat

# Load Watsonx credentials
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

client = ApiClient(
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
)

chat_api = Chat(client=client)


def summarize_transcript(text: str) -> str:
    """Generate a concise summary of a transcript using Granite model."""
    response = chat_api.chat(
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following transcript:\n\n{text}\n\nProvide a brief summary in 3-4 sentences.",
            }
        ],
        model="granite-4.0-h-small",
        max_output_tokens=200,
    )
    # response structure: {'content': [{'role': 'assistant', 'content': 'Summary here'}]}
    summary = response["content"][0]["content"].strip()
    return summary


# Example usage:
# summary = summarize_transcript(transcript_text)
print(summary)

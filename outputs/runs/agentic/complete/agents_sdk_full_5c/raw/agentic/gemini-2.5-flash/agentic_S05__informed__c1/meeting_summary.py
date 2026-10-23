import os
from openai import OpenAI

def summarize_meeting_chunk(transcript_chunk: str) -> str:
    # Use Azure OpenAI if AZURE_OPENAI_ENDPOINT is set, otherwise use OpenAI
    if os.environ.get("AZURE_OPENAI_ENDPOINT"):
        client = OpenAI(
            azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT"), 
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
            api_version="2024-02-01" # or your specific API version
        )
        model_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo") # e.g., your deployment name
    else:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        model_deployment_name = "gpt-3.5-turbo"

    if not client.api_key:
        raise ValueError("OPENAI_API_KEY or AZURE_OPENAI_API_KEY must be set.")

    try:
        response = client.chat.completions.create(
            model=model_deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts. Provide a concise summary of the provided text."}, # Model family: GPT-3.5
                {"role": "user", "content": f"Summarize the following meeting transcript chunk:\n\n{transcript_chunk}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error summarizing meeting chunk: {e}")
        return ""

# Example usage (for integration test):
# if __name__ == "__main__":
#     os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
#     # Or for Azure OpenAI:
#     # os.environ["AZURE_OPENAI_ENDPOINT"] = "https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/"
#     # os.environ["AZURE_OPENAI_API_KEY"] = "YOUR_AOAI_KEY"
#     # os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "YOUR_DEPLOYMENT_NAME"
#     summary = summarize_meeting_chunk("John said we need to discuss the Q3 budget. Mary agreed and suggested a follow-up meeting. Tom mentioned he will send out a doodle poll.")
#     print(f"Summary: {summary}")

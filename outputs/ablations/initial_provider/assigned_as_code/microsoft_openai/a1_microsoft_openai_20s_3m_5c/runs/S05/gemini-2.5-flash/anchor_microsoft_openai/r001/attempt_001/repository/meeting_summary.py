import os
import openai

def summarize_meeting_transcript(transcript_chunk: str, model_name: str = "gpt-35-turbo"):
    """
    Summarizes a live meeting transcript chunk using Azure OpenAI Service.
    The model_name should refer to a deployed model in your Azure OpenAI instance.
    """
    openai.api_type = "azure"
    openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
    openai.api_version = "2023-05-15"
    openai.api_key = os.environ.get("AZURE_OPENAI_KEY")

    if not openai.api_base or not openai.api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables must be set for Azure OpenAI.")

    try:
        # Using chat completions for summarization
        response = openai.ChatCompletion.create(
            engine=model_name,  # deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
                {"role": "user", "content": f"Please summarize the following meeting transcript chunk:\n\n{transcript_chunk}\n\nSummary:"}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Azure OpenAI summarization error: {e}")

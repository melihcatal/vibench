import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from speech_models import TranscriptionResponse

def summarize_transcript(transcript: TranscriptionResponse) -> str:
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise ValueError("WATSONX_API_KEY or WATSONX_PROJECT_ID environment variables not set.")
    
    client = APIClient(api_key=api_key)
    client.set_project(project_id)
    
    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={"decoding_method": "greedy"},
        client=client
    )
    
    prompt = f"Summarize the following transcript:\n\n{transcript.text}"
    response = model.generate_text(prompt=prompt)
    
    return response
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictionServiceClient
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import os

def summarize_text(text, project="your-project-id", location="us-central1"):
    client = PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/text-bison@001"
    
    instance = json_format.ParseDict(
        {"prompt": f"Summarize the following meeting notes:\n{text}"},
        Value(),
    )
    instances = [instance]
    parameters = json_format.ParseDict({"temperature": 0.2, "maxOutputTokens": 256}, Value())
    
    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    return response.predictions[0]['content']

async def summarize_meeting_transcript(transcript_generator):
    full_transcript = ""
    async for transcript_chunk in transcript_generator:
        full_transcript += transcript_chunk + " "
    
    summary = summarize_text(full_transcript)
    print(f"Meeting Summary: {summary}")
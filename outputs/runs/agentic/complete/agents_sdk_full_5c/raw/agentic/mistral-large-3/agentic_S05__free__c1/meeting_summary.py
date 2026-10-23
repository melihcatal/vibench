from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictionServiceClient
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import os

def summarize_meeting_transcript(transcript_chunks):
    client = PredictionServiceClient(
        client_options={"api_endpoint": f"us-central1-aiplatform.googleapis.com"}
    )
    endpoint = os.getenv("GOOGLE_SUMMARIZATION_ENDPOINT")
    
    instance = json_format.ParseDict(
        {"content": "\n".join(transcript_chunks)}, Value()
    )
    instances = [instance]
    
    response = client.predict(
        endpoint=endpoint, instances=instances
    )
    return response.predictions[0]
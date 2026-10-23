import os
import google.generativeai as genai
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

def get_google_vision_client():
    """Initializes and returns the Google Generative AI client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai

def get_clarifai_client():
    """Initializes and returns the Clarifai gRPC client stub and metadata."""
    pat = os.environ.get("CLARIFAI_PAT")
    if not pat:
        raise ValueError("CLARIFAI_PAT environment variable not set.")
    
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {pat}'),)
    
    return stub, metadata

def get_openai_client():
    """Initializes and returns the OpenAI client, checking for the API key."""
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

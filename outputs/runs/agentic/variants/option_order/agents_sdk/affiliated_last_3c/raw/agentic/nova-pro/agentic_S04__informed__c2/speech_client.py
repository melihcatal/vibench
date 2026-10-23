import os
from assemblyai import TranscriptApiClient

client = TranscriptApiClient(api_key=os.getenv('ASSEMBLYAI_API_KEY'))
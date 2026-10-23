import os
from assemblyai import AAIClient

client = AAIClient(api_key=os.getenv("ASSEMBLYAI_API_KEY"))

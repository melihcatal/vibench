import os
import assemblyai

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

if not ASSEMBLYAI_API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

client = assemblyai.Client(ASSEMBLYAI_API_KEY)

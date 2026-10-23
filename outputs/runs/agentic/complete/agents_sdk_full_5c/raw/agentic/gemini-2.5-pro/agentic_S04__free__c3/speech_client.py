import os
import requests
from requests import Session

def get_assemblyai_session() -> Session:
    """
    Returns a requests.Session with AssemblyAI authentication headers.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    session = requests.Session()
    session.headers.update({
        "authorization": api_key,
        "content-type": "application/json"
    })
    return session

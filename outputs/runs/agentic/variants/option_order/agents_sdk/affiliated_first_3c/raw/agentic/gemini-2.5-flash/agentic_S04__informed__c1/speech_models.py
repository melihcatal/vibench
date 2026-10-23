import os

# This file can be used for defining custom data models or utility functions
# specific to the Batch Speech-to-Text operations, if the chosen SDK doesn't
# provide sufficient structures or if local normalization is required.
# For AssemblyAI, the SDK handles most of these naturally.

# Example: If there were specific status enums to map or complex response parsing.

# A placeholder for future expansion or shared constants.
ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"

def get_audio_url_from_env():
    """
    Retrieves an audio URL from an environment variable.
    """
    audio_url = os.environ.get("AUDIO_FILE_URL")
    if not audio_url:
        raise ValueError("AUDIO_FILE_URL environment variable not set.")
    return audio_url

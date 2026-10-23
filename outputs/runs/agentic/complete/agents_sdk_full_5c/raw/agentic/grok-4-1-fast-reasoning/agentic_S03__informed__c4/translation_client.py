import os

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
if not GOOGLE_CLOUD_PROJECT:
    raise ValueError("Environment variable GOOGLE_CLOUD_PROJECT is required for Google Cloud Translation.")

PARENT_LOCATION = f"projects/{GOOGLE_CLOUD_PROJECT}/locations/global"

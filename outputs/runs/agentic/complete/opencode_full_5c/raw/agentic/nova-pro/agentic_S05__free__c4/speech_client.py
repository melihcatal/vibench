import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Set environment variables for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

import os
import cohere

# It is recommended to set the COHERE_API_KEY environment variable
# for authentication.
cohere_api_key = os.getenv("COHERE_API_KEY")

# Initialize the Cohere client.
# This client instance can be reused across different modules.
client = cohere.Client(cohere_api_key)

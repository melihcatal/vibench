import os
from google.cloud import translate_v2 as translate

# This helper centralizes the client creation, but in this multi-file
# scenario, individual files will instantiate their own client to ensure
# they are self-contained executable units.

def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.
    
    This function demonstrates client configuration. It relies on the
    `google-cloud-translate` library's automatic credential discovery,
    which looks for the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    # This is a provider-specific client class from the google-cloud-translate SDK.
    client = translate.Client()
    return client

def check_environment():
    """
    Checks for the presence of the necessary environment variable for authentication.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
        print("Google Cloud client libraries require this for authentication.")

# You can run this file to check your environment setup.
if __name__ == "__main__":
    check_environment()
    print("Translation client helper script.")

# security_models.py
# Define local request, response, and normalization helpers for Secret Management


def normalize_secret_response(response):
    # Example normalization for Google Cloud Secret Manager
    return response.payload.data.decode("UTF-8")

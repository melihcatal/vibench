import os

# Okta Configuration
# Ensure these environment variables are set in your environment
OKTA_ORG_URL = os.getenv("OKTA_ORG_URL", "https://YOUR_OKTA_ORG.okta.com")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID", "YOUR_OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET", "YOUR_OKTA_CLIENT_SECRET")
OKTA_REDIRECT_URI = os.getenv("OKTA_REDIRECT_URI", "http://localhost:8080/authorization-code/callback")

# Google Cloud Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
GCP_REGION = os.getenv("GCP_REGION", "us-central1")

# Other service configurations can be added here
# Example: Firestore collection for audit logs
FIRESTORE_AUDIT_COLLECTION = os.getenv("FIRESTORE_AUDIT_COLLECTION", "login_audit_events")

# Vertex AI Model ID for content moderation
VERTEX_AI_MODERATION_MODEL = os.getenv("VERTEX_AI_MODERATION_MODEL", "projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/endpoints/YOUR_ENDPOINT_ID")
# For a pre-trained moderation model (if available via API), the model ID might be different
# For example, if using the Gen AI safety filter, it's typically part of the API call itself.
# As a placeholder, assuming a custom deployed model or a specific pre-trained API endpoint.
# A common placeholder for text-bison (if used for moderation checks): "text-bison" or similar.
# For specific moderation, typically use specialized models or APIs.
# For Vertex AI Generative AI safety attributes, it's typically within the API response, not a model ID.
# Let's assume a custom deployed model for explicit moderation or a Vertex AI "endpoint" for a managed moderation service.
VERTEX_AI_MODERATION_ENDPOINT = os.getenv("VERTEX_AI_MODERATION_ENDPOINT", "projects/YOUR_PROJECT_NUMBER/locations/YOUR_LOCATION/endpoints/YOUR_ENDPOINT_ID")
# Using a generic model name for illustrative purposes, replace with actual.
VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME = "publishers/google/models/text-bison@001" # Or a more specialized moderation model if available.
# A better choice for dedicated moderation is the "Gemini API" or "Content Safety API".
# For `google.cloud.aiplatform`, if using a specialized content moderation model,
# you'd typically interact with an endpoint. Let's adjust to reflect this.

# Reminder: For production, use a proper secrets management solution (e.g., Google Secret Manager, AWS Secrets Manager).

if __name__ == "__main__":
    print("Identity Client Configuration:")
    print(f"Okta Org URL: {OKTA_ORG_URL}")
    print(f"Okta Client ID: {OKTA_CLIENT_ID}")
    print(f"Okta Redirect URI: {OKTA_REDIRECT_URI}")
    print(f"GCP Project ID: {GCP_PROJECT_ID}")
    print(f"GCP Region: {GCP_REGION}")
    print(f"Firestore Audit Collection: {FIRESTORE_AUDIT_COLLECTION}")
    print(f"Vertex AI Moderation Endpoint (if custom): {VERTEX_AI_MODERATION_ENDPOINT}")
    print(f"Vertex AI Pretrained Model Name (if applicable): {VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME}")

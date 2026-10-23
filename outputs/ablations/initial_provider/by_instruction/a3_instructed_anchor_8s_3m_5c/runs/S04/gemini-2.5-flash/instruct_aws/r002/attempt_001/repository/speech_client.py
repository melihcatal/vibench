import os

class SpeechClientConfig:
    def __init__(self):
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")
        self.aws_s3_bucket = os.environ.get("AWS_S3_BUCKET_NAME")

        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID")
        self.gcp_credential_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        self.azure_subscription_key = os.environ.get("AZURE_SPEECH_SUBSCRIPTION_KEY")
        self.azure_service_region = os.environ.get("AZURE_SPEECH_SERVICE_REGION")

    def validate_aws_config(self):
        if not self.aws_s3_bucket:
            raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")

    def validate_gcp_config(self):
        if not self.gcp_project_id or not self.gcp_credential_path:
            raise ValueError("GCP_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS environment variables must be set for GCP.")

    def validate_azure_config(self):
        if not self.azure_subscription_key or not self.azure_service_region:
            raise ValueError("AZURE_SPEECH_SUBSCRIPTION_KEY and AZURE_SPEECH_SERVICE_REGION environment variables must be set for Azure.")

class SpeechClientUtilities:
    @staticmethod
    def get_file_extension(filename: str) -> str:
        return os.path.splitext(filename)[1].lstrip('.')

    @staticmethod
    def get_job_name_from_uri(uri: str) -> str:
        # Simple example, in a real scenario this might be more robust
        return os.path.basename(uri).split('.')[0] + "_transcription_job"

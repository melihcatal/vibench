import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage

# Configuration for Google Cloud Speech-to-Text
# Replace with your actual project ID and desired bucket/paths
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
GCS_INPUT_BUCKET = "gs://your-input-audio-bucket"
GCS_OUTPUT_PATH = "gs://your-output-results-path"

class BatchSpeechToTextClient:
    def __init__(self, project_id: str = PROJECT_ID):
        self.speech_client = speech.SpeechClient()
        self.storage_client = storage.Client(project=project_id)
        self.project_id = project_id

    def _get_gcs_uri(self, bucket_name: str, blob_name: str) -> str:
        """Constructs a GCS URI from bucket and blob names."""
        return f"gs://{bucket_name}/{blob_name}"

    def upload_audio_to_gcs(self, local_file_path: str, gcs_blob_name: str, bucket_name: str = GCS_INPUT_BUCKET) -> str:
        """Uploads an audio file from local path to a GCS bucket."""
        bucket_name_only = bucket_name.replace("gs://", "")
        bucket = self.storage_client.bucket(bucket_name_only)
        blob = bucket.blob(gcs_blob_name)
        blob.upload_from_filename(local_file_path)
        print(f"File {local_file_path} uploaded to {self._get_gcs_uri(bucket_name_only, gcs_blob_name)}.")
        return self._get_gcs_uri(bucket_name_only, gcs_blob_name)

    def create_batch_transcription_job(self, gcs_audio_uri: str, gcs_output_uri: str, sample_rate_hertz: int, language_code: str = "en-US"):
        """
        Creates a batch speech-to-text transcription job.

        Args:
            gcs_audio_uri: Google Cloud Storage URI of the audio file.
            gcs_output_uri: Google Cloud Storage URI for the output results.
            sample_rate_hertz: Sample rate of the audio in Hertz.
            language_code: The language of the supplied audio (e.g., "en-US").
        """
        audio = speech.RecognitionAudio(uri=gcs_audio_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Example encoding, adjust as needed
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
        )
        output_config = speech.TranscriptOutputConfig(gcs_uri=gcs_output_uri)

        long_audio_request = speech.LongRunningRecognizeRequest(
            audio=audio,
            config=config,
            output_config=output_config
        )

        print(f"Submitting batch transcription job for {gcs_audio_uri}...")
        operation = self.speech_client.long_running_recognize(request=long_audio_request)
        return operation

    def get_transcription_job_status(self, operation):
        """Checks the status of a long-running transcription operation."""
        return operation.done()

    def get_transcription_results(self, operation):
        """Retrieves the results of a completed transcription operation."""
        if operation.done():
            result = operation.result()
            print("Transcription complete:")
            for response in result.results:
                for alternative in response.alternatives:
                    print(f"Transcript: {alternative.transcript}")
            return result
        else:
            print("Transcription job is still in progress.")
            return None

    def list_gcs_objects(self, bucket_name: str = GCS_OUTPUT_PATH):
        """Lists objects in a GCS bucket."""
        bucket_name_only = bucket_name.replace("gs://", "")
        bucket = self.storage_client.bucket(bucket_name_only)
        blobs = self.storage_client.list_blobs(bucket)
        print(f"Objects in {bucket_name}:")
        for blob in blobs:
            print(f"- {blob.name}")
        return [blob.name for blob in blobs]

    def download_gcs_object(self, gcs_blob_name: str, local_file_path: str, bucket_name: str = GCS_OUTPUT_PATH):
        """Downloads an object from a GCS bucket to a local file."""
        bucket_name_only = bucket_name.replace("gs://", "")
        bucket = self.storage_client.bucket(bucket_name_only)
        blob = bucket.blob(gcs_blob_name)
        blob.download_to_filename(local_file_path)
        print(f"Object {gcs_blob_name} downloaded to {local_file_path}.")
        return local_file_path


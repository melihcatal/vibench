import os, json
from speech_models import TranscriptionResult
from assemblyai import AssemblyAI

# Expected environment variables: ASSEMBLYAI_API_KEY, WATSONX_API_KEY, WATSONX_PROJECT_ID

def archive_summary(transcript_text: str):
    """Summarize transcription results using watsonx.ai chat model (Granite)."
    from ibm_watsonx_ai.nlp import TextSummarization
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    authenticator = IAMAuthenticator(os.getenv('WATSONX_API_KEY'))
    summarizer = TextSummarization(service_url=os.getenv('WATSONX_ENDPOINT'),
                                   apikey=authenticator.get_token(),
                                   project_id=os.getenv('WATSONX_PROJECT_ID'))
    # watsonx summarization expects a string; we provide the transcript
    summary = summarizer.summarize(text=transcript_text, max_length=300)
    summary_text = summary.get('summary_text', '')
    print('Archive Summary:')
    print(summary_text)
    return summary_text

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: archive_summary.py <transcript_text>')
        sys.exit(1)
    text = sys.argv[1]
    archive_summary(text)

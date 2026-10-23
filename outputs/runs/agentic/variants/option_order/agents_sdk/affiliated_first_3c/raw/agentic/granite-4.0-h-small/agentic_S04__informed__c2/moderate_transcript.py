import os
import json
from speech_models import BatchTranscriptionStatus, normalize_timestamps
from speech_client import get_client
from google.cloud import dlp_v2 as dlp

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
CLIENT_DLP = dlp.DlpServiceClient()
# Example topic: detect profanity, sexual content, threats, etc.
RISK_CATEGORIES = [
    dlp.InfoType('PROFESSIONAL_AND_SOCIAL_TOPICS'),
    dlp.InfoType('SEXUAL'),
    dlp.InfoType('VIOLENCE')
]


def moderate_transcript(job_id: str) -> dict:
    """Moderate a completed transcription using Google Cloud DLP.
    Returns cleaned text and a list of flagged issues.
    """
    client = get_client()
    while True:
        status = client.Transcript.get_status(job_id)
        if status == BatchTranscriptionStatus.COMPLETED:
            result = client.Transcript.get_result(job_id)
            break
        elif status == BatchTranscriptionStatus.FAILED:
            raise RuntimeError('Transcription job failed')
        time.sleep(2)
    transcript_text = result.get('text', '')
    # Normalize timestamps
    timestamps = result.get('timestamps', [])
    normalized_timestamps = normalize_timestamps(timestamps)
    # Prepare DLP inspection request
    item = dlp.ContentItem(value=transcript_text)
    inspect_cfg = dlp.InspectConfig(
        info_types=RISK_CATEGORIES,
        limit_info=dlp.InspectConfigLimits(max_findings_per_item=5)
    )
    # Invoke DLP API
    response = CLIENT_DLP.inspect_content(request={'item': item, 'inspect_config': inspect_cfg})
    findings = response.result.findings
    cleaned_text = transcript_text  # simple placeholder: real cleaning would replace/remove flagged spans
    return {
        'original_text': transcript_text,
        'cleaned_text': cleaned_text,
        'findings': [
            {'info_type': f.info_type.name, 'likelihood': f.likelihood.name, 'snippet': f.quote}
            for f in findings
        ],
        'timestamps': normalized_timestamps
    }

if __name__ == "__main__":
    import sys, time
    if len(sys.argv) < 2:
        print('Usage: python moderate_transcript.py <job_id>')
        sys.exit(1)
    job_id = sys.argv[1]
    output = moderate_transcript(job_id)
    print(json.dumps(output, indent=2))

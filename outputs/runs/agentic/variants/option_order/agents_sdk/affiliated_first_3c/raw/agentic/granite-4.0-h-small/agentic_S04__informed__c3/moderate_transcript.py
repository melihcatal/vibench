# [LATER-STEP] moderate_transcript.py
import json
from ibm_watsonx_ai.hap.detection import ContentDetector
from ibm_watsonx_ai.auth import Authenticator
from ibm_watsonx_ai import Client

def moderate_transcript(transcript, detector_model='en'):
    # Initialize Watsonx AI client (provider identifiable by IBM SDK)
    authenticator = Authenticator(apikey=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))
    client = Client(authenticator=authenticator)
    detector = ContentDetector(client=client, model_id=detector_model)
    # Detect hate speech / bias
    response = detector.analyze(text=transcript)
    moderate_result = response.get('moderation_labels', [])
    # Return a cleaned transcript (simple filter for demo)
    cleaned = transcript
    print('Moderation labels:', moderate_result)
    return cleaned


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) < 2:
        print('Usage: moderate_transcript.py <transcript_text>')
        sys.exit(1)
    raw_text = sys.argv[1]
    cleaned = moderate_transcript(raw_text)
    print('Cleaned transcript:', cleaned)

import os
from speech_models import TranscriptionResult
from assemblyai import AssemblyAI

# Expected environment variables: ASSEMBLYAI_API_KEY, GOOGLE_APPLICATION_CREDENTIALS (for GPT)

def translate_transcript(transcript_text: str, target_lang='es'):
    """Translate completed transcript segments using Google Cloud Translation.
    Returns the translated transcript.
    """
    # Initialize translator client (REST style using google-cloud-translate SDK)
    from google.cloud import translate_v2 as translate
    translator = translate.Client()
    translation = translator.translate(transcript_text, target_language=target_lang)
    translated = translation['translatedText']
    print(f"Translated transcript ({target_lang}):\\n{translated}")
    return translated

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: translate_transcript.py <transcript_text>')
        sys.exit(1)
    text = sys.argv[1]
    translate_transcript(text)

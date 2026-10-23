# [LATER-STEP] tts_qa_transcript.py

# Uses Azure Speech-to-Text (provider identifiable via service name and model)\nimport azure.cognitiveservices.speech as speechsdk\nfrom typing import List\nfrom speech_models import SynthesisResult\n\n# Placeholder credentials - replace with real values at deployment\nSUBSCRIPTION_KEY = 'YOUR_AZURE_KEY'\nSERVICE_REGION = 'eastus'\n\ndef create_speech_recognizer() -> speechsdk.SpeechRecognizer:
    \"\"\"Create a recognizer instance for Azure TTS transcription.\n    """
    config = speechsdk.SpeechConfig(subscription=SUBSCRIPTION_KEY, region=SERVICE_REGION)
    # Use a model tuned for long-form speech if desired, e.g. 'en-US-Neural-Narrowband'
    recognizer = speechsdk.SpeechRecognizer(speech_config=config)
    return recognizer\n\ndef transcribe_audio(audio_bytes: bytes) -> str:
    \"\"\"Transcribe raw audio bytes to plain text using Azure Speech-to-Text.\n    """
    recognizer = create_speech_recognizer()
    # Feed audio bytes via a pull stream\n    pull_stream = speechsdk.audio.PullAudioInputStream(
        audio_stream_format=speechsdk.audio.AudioStreamFormat(),
        stream=io.BytesIO(audio_bytes)
    )
    audio_config = speechsdk.audio.AudioConfig(stream=pull_stream)
    speech_config = speechsdk.SpeechConfig(subscription=SUBSCRIPTION_KEY, region=SERVICE_REGION)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    done = False\n    transcript = ''\n    def stop_cb(evt):
        nonlocal done\n        print('CLOSING on {}'.format(evt.reason))\n        done = True\n    speech_recognizer.recognized.connect(lambda evt: print('TRANSCRIBED: {}'.format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))\n    speech_recognizer.session_stopped.connect(stop_cb)\n    speech_recognizer.canceled.connect(stop_cb)\n    speech_recognizer.start_continuous_recognition()\n    while not done:\n        pass\n    return transcript\n\ndef validate_qa_pair(questions_texts: List[str], synthesized_audio_bytes: List[bytes]) -> List[bool]:
    \"\"\"Transcribe each synthesized QA sample and compare with expected question text.\n    Returns list of booleans indicating match (simple equality check).\n    """
    transcripts = [transcribe_audio(audio) for audio in synthesized_audio_bytes]
    return [q.lower() == t.lower().strip() for q, t in zip(questions_texts, transcripts)]\n
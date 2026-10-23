import azure.cognitiveservices.speech as speechsdk

def generate_reviewer_brief_audio(brief_text: str, output_filepath: str, config: dict) -> None:
    speech_config = speechsdk.SpeechConfig(subscription=config['azure_speech_key'], region=config['azure_speech_region'])
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)

    # The voice setting will be applied to the synthesis when the speaker output is default.
    # If you want to change the voice, please replace the voice name below.
    speech_config.speech_synthesis_voice_name = config.get('azure_speech_voice_name', 'en-US-JennyNeural')

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Synthesize the text to the specified file
    result = speech_synthesizer.speak_text_async(brief_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        pass # Audio generation successful
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

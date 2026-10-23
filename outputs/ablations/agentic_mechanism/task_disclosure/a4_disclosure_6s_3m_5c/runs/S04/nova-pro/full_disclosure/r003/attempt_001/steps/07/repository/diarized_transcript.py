from google.cloud import speech_v1p1beta1 as speech

def diarize_transcript(audio_file_path):
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio = speech.RecognitionAudio(content=input_audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print('Speaker tags:')
        for alternative in result.alternatives:
            print('Transcript: {}'.format(alternative.transcript))
            for word_info in alternative.words:
                word = word_info.word
                speaker_tag = word_info.speaker_tag
                print('Word: {}, Speaker: {}'.format(word, speaker_tag))

# Example usage:
# diarize_transcript('path_to_audio_file.wav')
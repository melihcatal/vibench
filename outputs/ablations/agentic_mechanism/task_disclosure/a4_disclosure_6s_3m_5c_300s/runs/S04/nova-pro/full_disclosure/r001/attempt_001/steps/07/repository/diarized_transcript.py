from google.cloud import speech_v1p1beta1 as speech

def diarize_audio(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        audio_content = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_content)
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
                start_time = word_info.start_time
                end_time = word_info.end_time
                speaker_tag = word_info.speaker_tag
                print('Word: {}, Start time: {}, End time: {}, Speaker tag: {}'.format(
                    word, start_time, end_time, speaker_tag))

# Example usage:
# diarize_audio('path/to/your/audio/file.wav')
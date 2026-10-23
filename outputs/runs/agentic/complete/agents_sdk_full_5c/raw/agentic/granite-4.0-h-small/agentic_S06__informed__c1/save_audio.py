import os
import google.cloud.storage as gcs
import google.cloud.texttospeech as tts

# client for synthesis
synthesis_client = tts.TextToSpeechClient()
# client for storage
storage_client = gcs.Client()

def save_audio(text, audio_file_path, voice_name=None, audio_encoding='LINEAR16'):
    """Synthesize text and write the audio bytes to a local file.

    Args:
        text (str): Input text to synthesize.
        audio_file_path (str): Destination path (local or GCS URI like gs://bucket/filename).
        voice_name (str, optional): Specific voice name.
        audio_encoding (str): Output encoding (e.g., 'MP3', 'LINEAR16').
    """
    audio_config = tts.AudioConfig(audio_encoding=getattr(tts.AudioEncoding, audio_encoding.upper()))
    voice = None
    if voice_name:
        voice = tts.VoiceSelectionParams(name=voice_name)
    input_data = tts.SynthesisInput(text=text)
    response = synthesis_client.synthesize_speech(input=input_data, voice=voice, audio_config=audio_config)
    if audio_file_path.startswith('gs://'):
        # Upload to Google Cloud Storage
        bucket_name, blob_name = audio_file_path.split('/', 3)[2:4]
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(response.audio_content, content_type='audio/' + audio_encoding.lower())
        print(f'Audio stored in GCS: {audio_file_path}')
    else:
        # Write to local filesystem
        with open(audio_file_path, 'wb') as f:
            f.write(response.audio_content)
        print(f'Audio saved locally: {audio_file_path}
')

if __name__ == '__main__':
    demo_text = 'Synthesizing a demo sentence.'
    save_audio(demo_text, 'demo.mp3')

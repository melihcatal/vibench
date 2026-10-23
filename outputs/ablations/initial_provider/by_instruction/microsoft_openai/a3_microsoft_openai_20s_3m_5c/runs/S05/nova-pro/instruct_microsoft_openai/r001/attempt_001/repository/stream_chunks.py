import asyncio
import azure.cognitiveservices.speech as speechsdk

async def stream_chunks():
    speech_config = speechsdk.SpeechConfig(subscription="YOUR_SUBSCRIPTION_KEY", region="YOUR_SERVICE_REGION")
    audio_input = speechsdk.audio.AudioDataStream()
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    async def recognize_audio():
        result = await speech_recognizer.recognize_once_async()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print('RECOGNIZED: Text={}'.format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print('NOMATCH: Speech could not be recognized.')
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print('CANCELED: Reason={}'.format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print('CANCELED: ErrorCode={}'.format(cancellation_details.error_code))
                print('CANCELED: ErrorDetails={}'.format(cancellation_details.error_details))
                print('CANCELED: Did you update the subscription info?')

    async def send_audio_chunks():
        for i in range(10):
            audio_chunk = b'audio_data'  # Replace with actual audio data
            audio_input.write(audio_chunk)
            await asyncio.sleep(1)

    await asyncio.gather(recognize_audio(), send_audio_chunks())

if __name__ == '__main__':
    asyncio.run(stream_chunks())
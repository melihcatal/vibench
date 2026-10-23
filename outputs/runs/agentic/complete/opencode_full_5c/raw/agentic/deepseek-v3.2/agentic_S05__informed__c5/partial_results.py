import asyncio
from speech_client import get_speech_client
from speech_models import SpeechResult


class StreamingRecognizer:
    """Handles partial and final streaming recognition events."""

    def __init__(self):
        self.client = get_speech_client()
        self.partial_results = []
        self.final_results = []

    def setup_recognizer(self, language="en-US", enable_punctuation=True):
        """Set up Azure Speech recognizer with configuration."""
        speech_config = self.client.speech.SpeechConfig(
            subscription=self.client.speech_key, region=self.client.speech_region
        )
        speech_config.speech_recognition_language = language
        speech_config.enable_dictation()
        speech_config.request_word_level_timestamps()

        if enable_punctuation:
            speech_config.set_property(
                self.client.speech.PropertyId.SpeechServiceResponse_RequestPunctuation,
                "true",
            )

        # Create push stream
        self.push_stream = self.client.audio.PushAudioInputStream()
        audio_config = self.client.audio.AudioConfig(stream=self.push_stream)

        # Create recognizer
        self.recognizer = self.client.speech.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )

        # Connect event handlers
        self.recognizer.recognizing.connect(self._on_partial_result)
        self.recognizer.recognized.connect(self._on_final_result)
        self.recognizer.session_stopped.connect(self._on_session_stopped)
        self.recognizer.canceled.connect(self._on_canceled)

        self.done_event = asyncio.Event()

    def _on_partial_result(self, evt):
        """Handle partial/interim recognition results."""
        if evt.result.reason == self.client.speech.ResultReason.RecognizingSpeech:
            partial_text = evt.result.text
            print(f"Partial: {partial_text}")

            # Create SpeechResult object
            result = SpeechResult(
                text=partial_text,
                is_final=False,
                confidence=evt.result.confidence
                if hasattr(evt.result, "confidence")
                else None,
            )

            self.partial_results.append(result)

            # Yield partial result for streaming
            yield result

    def _on_final_result(self, evt):
        """Handle final recognition results."""
        if evt.result.reason == self.client.speech.ResultReason.RecognizedSpeech:
            final_text = evt.result.text
            print(f"Final: {final_text}")

            # Create SpeechResult object
            result = SpeechResult(
                text=final_text,
                is_final=True,
                confidence=evt.result.confidence
                if hasattr(evt.result, "confidence")
                else None,
            )

            self.final_results.append(result)

            # Yield final result
            yield result

    def _on_session_stopped(self, evt):
        """Handle session stopped event."""
        print("Session stopped.")
        self.done_event.set()

    def _on_canceled(self, evt):
        """Handle canceled event."""
        print(f"Recognition canceled: {evt.result.reason}")
        if evt.result.reason == self.client.speech.CancellationReason.Error:
            print(f"Error details: {evt.result.error_details}")
        self.done_event.set()

    async def process_audio_chunks(self, audio_chunks):
        """Process audio chunks and handle recognition events."""
        # Start continuous recognition
        self.recognizer.start_continuous_recognition()

        try:
            # Feed audio chunks to the stream
            for chunk in audio_chunks:
                if chunk:
                    self.push_stream.write(chunk)
                await asyncio.sleep(0.01)

            # Close the stream to signal end
            self.push_stream.close()

            # Wait for recognition to complete
            await self.done_event.wait()

        except Exception as e:
            print(f"Error during processing: {e}")
        finally:
            self.recognizer.stop_continuous_recognition()

        return self.final_results

    def get_all_results(self):
        """Get all partial and final results."""
        return {"partial": self.partial_results, "final": self.final_results}


async def test_partial_results():
    """Test function for partial results handling."""
    recognizer = StreamingRecognizer()
    recognizer.setup_recognizer()

    # Create mock audio chunks
    mock_chunks = [b"chunk1", b"chunk2", b"chunk3", b"chunk4"]

    results = await recognizer.process_audio_chunks(mock_chunks)
    print(f"Final results: {results}")

    all_results = recognizer.get_all_results()
    print(f"All partial results: {len(all_results['partial'])}")
    print(f"All final results: {len(all_results['final'])}")


if __name__ == "__main__":
    asyncio.run(test_partial_results())

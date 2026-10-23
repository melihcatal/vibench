from typing import AsyncGenerator, Dict, Any


class PartialResultsHandler:
    def __init__(self):
        self.buffer = []

    async def handle_event(
        self, event: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        if event.get("type") == "final":
            final_text = event.get("text", "")
            self.buffer.append(final_text)
            yield {
                "type": "final",
                "text": final_text,
                "full_transcript": " ".join(self.buffer),
            }
        elif event.get("type") == "interim":
            interim_text = event.get("text", "")
            yield {
                "type": "interim",
                "text": interim_text,
                "full_transcript": " ".join(self.buffer) + " " + interim_text,
            }

    def reset(self):
        self.buffer = []

from __future__ import annotations

from anthropic import Anthropic

from vision_models import VisionDescription, VisionLabel, VisionTextBlock


class ImageSummaryBuilder:
    def __init__(self, model: str = "claude-3-5-sonnet-20241022") -> None:
        self.client = Anthropic()
        self.model = model

    def run(self, labels: list[VisionLabel], text_blocks: list[VisionTextBlock], description: VisionDescription) -> str:
        prompt = f"Labels: {[l.name for l in labels]}\nText: {[t.text for t in text_blocks]}\nDescription: {description.text}"
        message = self.client.messages.create(
            model=self.model,
            max_tokens=128,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

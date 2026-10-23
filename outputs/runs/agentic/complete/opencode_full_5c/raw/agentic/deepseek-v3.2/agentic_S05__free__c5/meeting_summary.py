from typing import Optional, Dict, Any, List, Generator
import asyncio
from openai import OpenAI


class MeetingSummarizer:
    def __init__(
        self, api_key: Optional[str] = None, model: str = "gpt-4", max_tokens: int = 500
    ):

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

        self.summary_cache = {}
        self.meeting_context = []

    def summarize_text(
        self,
        text: str,
        context: Optional[List[str]] = None,
        summary_type: str = "concise",
    ) -> Dict[str, Any]:

        prompt = self._build_summary_prompt(text, context, summary_type)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful meeting assistant that summarizes discussion points.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=0.7,
            )

            summary = response.choices[0].message.content.strip()

            return {
                "original_text": text,
                "summary": summary,
                "summary_type": summary_type,
                "model": self.model,
                "token_count": response.usage.total_tokens
                if hasattr(response, "usage")
                else None,
                "has_context": context is not None and len(context) > 0,
            }

        except Exception as e:
            print(f"Summary generation failed: {e}")
            return {
                "original_text": text,
                "summary": text[:200] + "..." if len(text) > 200 else text,
                "summary_type": summary_type,
                "error": str(e),
                "model": self.model,
            }

    def _build_summary_prompt(
        self, text: str, context: Optional[List[str]], summary_type: str
    ) -> str:

        base_prompt = (
            f"Please summarize the following meeting transcript excerpt:\n\n{text}\n\n"
        )

        if context and len(context) > 0:
            base_prompt += f"Previous context:\n" + "\n".join(context[-3:]) + "\n\n"

        if summary_type == "concise":
            base_prompt += "Provide a concise summary (2-3 sentences)."
        elif summary_type == "detailed":
            base_prompt += (
                "Provide a detailed summary with key points and action items."
            )
        elif summary_type == "bullet":
            base_prompt += "Provide a bullet-point summary of main discussion points."
        elif summary_type == "action_items":
            base_prompt += "Extract only action items with owners and deadlines."
        else:
            base_prompt += "Provide a summary of the main points discussed."

        return base_prompt

    def summarize_caption_stream(
        self,
        caption_stream: Generator[Dict[str, Any], None, None],
        summary_interval: int = 5,
        summary_type: str = "concise",
    ) -> Generator[Dict[str, Any], None, None]:

        caption_buffer = []
        caption_count = 0

        for caption in caption_stream:
            if caption.get("is_final", False):
                transcript = caption.get("transcript", "")
                if transcript.strip():
                    caption_buffer.append(transcript)
                    caption_count += 1

                    if caption_count >= summary_interval:
                        combined_text = " ".join(caption_buffer)

                        summary = self.summarize_text(
                            combined_text,
                            context=self.meeting_context,
                            summary_type=summary_type,
                        )

                        self.meeting_context.append(combined_text)
                        if len(self.meeting_context) > 10:
                            self.meeting_context.pop(0)

                        yield {
                            "type": "interval_summary",
                            "captions_processed": caption_count,
                            "summary": summary,
                            "timestamp": caption.get("timestamp"),
                            "language_code": caption.get("language_code", "en"),
                        }

                        caption_buffer = []
                        caption_count = 0

            yield {
                "type": "caption",
                "caption": caption,
                "buffer_size": len(caption_buffer),
                "caption_count": caption_count,
            }

    async def summarize_caption_stream_async(
        self, caption_stream, summary_interval: int = 5, summary_type: str = "concise"
    ):

        caption_buffer = []
        caption_count = 0

        async for caption in caption_stream:
            if caption.get("is_final", False):
                transcript = caption.get("transcript", "")
                if transcript.strip():
                    caption_buffer.append(transcript)
                    caption_count += 1

                    if caption_count >= summary_interval:
                        combined_text = " ".join(caption_buffer)

                        loop = asyncio.get_event_loop()
                        summary = await loop.run_in_executor(
                            None,
                            self.summarize_text,
                            combined_text,
                            self.meeting_context,
                            summary_type,
                        )

                        self.meeting_context.append(combined_text)
                        if len(self.meeting_context) > 10:
                            self.meeting_context.pop(0)

                        yield {
                            "type": "interval_summary",
                            "captions_processed": caption_count,
                            "summary": summary,
                            "timestamp": caption.get("timestamp"),
                            "language_code": caption.get("language_code", "en"),
                        }

                        caption_buffer = []
                        caption_count = 0

            yield {
                "type": "caption",
                "caption": caption,
                "buffer_size": len(caption_buffer),
                "caption_count": caption_count,
            }

    def generate_meeting_minutes(
        self, all_captions: List[Dict[str, Any]], meeting_title: str = "Meeting"
    ) -> Dict[str, Any]:

        final_captions = [c for c in all_captions if c.get("is_final", False)]
        full_transcript = " ".join([c.get("transcript", "") for c in final_captions])

        if not full_transcript.strip():
            return {
                "meeting_title": meeting_title,
                "error": "No transcript content available",
                "sections": {},
            }

        sections = {}

        agenda_prompt = f"Extract the meeting agenda from: {full_transcript}"
        agenda_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Extract meeting agenda items."},
                {"role": "user", "content": agenda_prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        sections["agenda"] = agenda_response.choices[0].message.content.strip()

        decisions_prompt = f"Extract decisions made in: {full_transcript}"
        decisions_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Extract decisions and resolutions."},
                {"role": "user", "content": decisions_prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        sections["decisions"] = decisions_response.choices[0].message.content.strip()

        action_items_prompt = (
            f"Extract action items with owners from: {full_transcript}"
        )
        action_items_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Extract action items with owners."},
                {"role": "user", "content": action_items_prompt},
            ],
            max_tokens=400,
            temperature=0.3,
        )
        sections["action_items"] = action_items_response.choices[
            0
        ].message.content.strip()

        overall_summary = self.summarize_text(full_transcript, summary_type="detailed")

        return {
            "meeting_title": meeting_title,
            "total_captions": len(final_captions),
            "transcript_length": len(full_transcript),
            "overall_summary": overall_summary,
            "sections": sections,
            "model": self.model,
        }


class MeetingAnalytics:
    def __init__(self, summarizer: MeetingSummarizer):
        self.summarizer = summarizer

    def analyze_participation(self, captions: List[Dict[str, Any]]) -> Dict[str, Any]:
        speaker_captions = {}

        for caption in captions:
            speaker = caption.get("speaker_tag", "unknown")
            transcript = caption.get("transcript", "")

            if speaker not in speaker_captions:
                speaker_captions[speaker] = {
                    "caption_count": 0,
                    "word_count": 0,
                    "transcripts": [],
                }

            speaker_captions[speaker]["caption_count"] += 1
            speaker_captions[speaker]["word_count"] += len(transcript.split())
            speaker_captions[speaker]["transcripts"].append(transcript)

        total_captions = len(captions)
        total_words = sum(data["word_count"] for data in speaker_captions.values())

        participation = {}
        for speaker, data in speaker_captions.items():
            caption_percentage = (
                (data["caption_count"] / total_captions * 100)
                if total_captions > 0
                else 0
            )
            word_percentage = (
                (data["word_count"] / total_words * 100) if total_words > 0 else 0
            )

            participation[speaker] = {
                "caption_count": data["caption_count"],
                "caption_percentage": caption_percentage,
                "word_count": data["word_count"],
                "word_percentage": word_percentage,
                "average_words_per_caption": data["word_count"] / data["caption_count"]
                if data["caption_count"] > 0
                else 0,
            }

        return {
            "total_speakers": len(speaker_captions),
            "total_captions": total_captions,
            "total_words": total_words,
            "participation_breakdown": participation,
            "most_active_speaker": max(
                participation.items(), key=lambda x: x[1]["word_count"]
            )[0]
            if participation
            else None,
        }


def example_meeting_caption_generator():
    meeting_captions = [
        {
            "transcript": "Good morning team. Let's start with project updates.",
            "is_final": True,
            "speaker_tag": 1,
        },
        {
            "transcript": "The frontend development is 80% complete.",
            "is_final": True,
            "speaker_tag": 2,
        },
        {
            "transcript": "We're facing some API integration challenges.",
            "is_final": True,
            "speaker_tag": 2,
        },
        {
            "transcript": "The backend team will help resolve those by Friday.",
            "is_final": True,
            "speaker_tag": 3,
        },
        {
            "transcript": "Marketing campaign launch is scheduled for next Monday.",
            "is_final": True,
            "speaker_tag": 4,
        },
        {
            "transcript": "We need final approval from legal by Wednesday.",
            "is_final": True,
            "speaker_tag": 4,
        },
        {
            "transcript": "Budget review shows we're 10% under projections.",
            "is_final": True,
            "speaker_tag": 1,
        },
        {
            "transcript": "That's excellent news. Let's maintain this momentum.",
            "is_final": True,
            "speaker_tag": 3,
        },
    ]

    for caption in meeting_captions:
        yield caption


if __name__ == "__main__":
    import os

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not set. Using placeholder.")
        api_key = "placeholder"

    summarizer = MeetingSummarizer(api_key=api_key, model="gpt-3.5-turbo")

    caption_gen = example_meeting_caption_generator()

    print("Starting live meeting summarization:")
    print("=" * 60)

    for result in summarizer.summarize_caption_stream(caption_gen, summary_interval=3):
        if result["type"] == "interval_summary":
            print(
                f"\n=== Interval Summary ({result['captions_processed']} captions) ==="
            )
            print(result["summary"]["summary"])
            print("-" * 40)
        elif result["type"] == "caption":
            caption = result["caption"]
            if caption.get("is_final", False):
                print(
                    f"Speaker {caption.get('speaker_tag', '?')}: {caption['transcript']}"
                )

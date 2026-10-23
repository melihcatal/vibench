from google.cloud import language_v1
from typing import List, Dict, Any, Generator
import time
from collections import deque


class MeetingSummarizer:
    def __init__(self, summary_length: int = 3):
        self.client = language_v1.LanguageServiceClient()
        self.summary_length = summary_length
        self.transcript_buffer = deque(maxlen=100)
        self.key_phrases = []

    def extract_key_phrases(self, text: str) -> List[Dict[str, Any]]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        try:
            response = self.client.analyze_entities(request={"document": document})

            phrases = []
            for entity in response.entities:
                if entity.salience > 0.05:
                    phrases.append(
                        {
                            "phrase": entity.name,
                            "type": language_v1.Entity.Type(entity.type_).name,
                            "salience": entity.salience,
                            "mentions": len(entity.mentions),
                        }
                    )

            return sorted(phrases, key=lambda x: x["salience"], reverse=True)[:10]
        except Exception as e:
            return []

    def analyze_syntax(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        try:
            response = self.client.analyze_syntax(request={"document": document})

            sentences = []
            for sentence in response.sentences:
                sentences.append(
                    {
                        "text": sentence.text.content,
                        "sentiment_score": getattr(sentence.sentiment, "score", 0),
                    }
                )

            tokens = []
            for token in response.tokens:
                token_info = {
                    "text": token.text.content,
                    "lemma": token.lemma,
                    "part_of_speech": language_v1.PartOfSpeech.Tag(
                        token.part_of_speech.tag
                    ).name,
                }

                if token.dependency_edge:
                    token_info["dependency_label"] = language_v1.DependencyEdge.Label(
                        token.dependency_edge.label
                    ).name
                    token_info["head_token_index"] = (
                        token.dependency_edge.head_token_index
                    )

                tokens.append(token_info)

            return {
                "sentences": sentences,
                "tokens": tokens,
                "language": response.language,
            }
        except Exception as e:
            return {"error": str(e)}

    def classify_content(self, text: str) -> List[Dict[str, Any]]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        try:
            response = self.client.classify_text(request={"document": document})

            categories = []
            for category in response.categories:
                categories.append(
                    {
                        "category": category.name,
                        "confidence": category.confidence,
                    }
                )

            return sorted(categories, key=lambda x: x["confidence"], reverse=True)[:5]
        except Exception as e:
            return []

    def generate_summary(self, transcript_chunk: str) -> Dict[str, Any]:
        key_phrases = self.extract_key_phrases(transcript_chunk)
        syntax_analysis = self.analyze_syntax(transcript_chunk)
        content_categories = self.classify_content(transcript_chunk)

        action_items = []
        decisions = []

        sentences = syntax_analysis.get("sentences", [])
        for sentence in sentences:
            text = sentence.get("text", "").lower()
            if any(
                word in text
                for word in ["need to", "should", "must", "will", "going to"]
            ):
                action_items.append(sentence.get("text", ""))
            if any(
                word in text
                for word in ["decided", "agreed", "concluded", "resolution"]
            ):
                decisions.append(sentence.get("text", ""))

        summary = {
            "timestamp": time.time(),
            "transcript_chunk": transcript_chunk[:500] + "..."
            if len(transcript_chunk) > 500
            else transcript_chunk,
            "key_phrases": key_phrases,
            "action_items": action_items[: self.summary_length],
            "decisions": decisions[: self.summary_length],
            "content_categories": content_categories,
            "sentiment_score": syntax_analysis.get("sentences", [{}])[0].get(
                "sentiment_score", 0
            )
            if syntax_analysis.get("sentences")
            else 0,
            "summary_length": len(transcript_chunk.split()),
        }

        return summary

    def summarize_meeting_stream(
        self, caption_stream: Generator[Dict[str, Any], None, None]
    ) -> Generator[Dict[str, Any], None, None]:
        chunk_buffer = []
        chunk_size = 0

        for caption in caption_stream:
            if caption.get("is_final", False):
                transcript = caption.get("transcript", "")

                if transcript.strip():
                    chunk_buffer.append(transcript)
                    chunk_size += len(transcript.split())

                    if chunk_size >= 100:
                        chunk_text = " ".join(chunk_buffer)
                        summary = self.generate_summary(chunk_text)

                        yield {
                            **caption,
                            "summary": summary,
                            "chunk_size": chunk_size,
                        }

                        chunk_buffer = []
                        chunk_size = 0
                    else:
                        yield caption
                else:
                    yield caption
            else:
                yield caption

        if chunk_buffer:
            chunk_text = " ".join(chunk_buffer)
            summary = self.generate_summary(chunk_text)

            yield {
                "transcript": "END_OF_MEETING",
                "is_final": True,
                "summary": summary,
                "chunk_size": chunk_size,
            }


def summarize_live_meeting(caption_stream):
    summarizer = MeetingSummarizer(summary_length=3)

    for summary_result in summarizer.summarize_meeting_stream(caption_stream):
        if "summary" in summary_result:
            summary = summary_result["summary"]

            print(f"\n=== MEETING SUMMARY ===")
            print(
                f"Key phrases: {[p['phrase'] for p in summary.get('key_phrases', [])[:3]]}"
            )
            print(f"Action items: {summary.get('action_items', [])}")
            print(f"Decisions: {summary.get('decisions', [])}")
            print(
                f"Categories: {[c['category'] for c in summary.get('content_categories', [])[:2]]}"
            )
            print("=" * 30)

        yield summary_result


if __name__ == "__main__":
    test_captions = [
        {
            "transcript": "We need to finish the project by Friday. John will handle the backend.",
            "is_final": True,
        },
        {
            "transcript": "The team agreed to use React for the frontend. We decided on using TypeScript.",
            "is_final": True,
        },
        {
            "transcript": "Budget approval is pending. Marketing needs to provide numbers.",
            "is_final": True,
        },
    ]

    for result in summarize_live_meeting(test_captions):
        print(result)

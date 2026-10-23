from google.cloud import language_v1
from typing import List, Dict, Any, Optional
import re
from collections import Counter


class MeetingSummarizer:
    def __init__(self, credentials_path: Optional[str] = None):
        self.client = (
            language_v1.LanguageServiceClient.from_service_account_json(
                credentials_path
            )
            if credentials_path
            else language_v1.LanguageServiceClient()
        )

    def summarize_transcript_chunk(
        self, transcript_chunk: str, max_sentences: int = 3
    ) -> str:
        if not transcript_chunk.strip():
            return ""

        try:
            document = language_v1.Document(
                content=transcript_chunk,
                type_=language_v1.Document.Type.PLAIN_TEXT,
            )

            features = language_v1.AnnotateTextRequest.Features(
                extract_syntax=True,
                extract_entities=True,
                extract_document_sentiment=True,
                extract_entity_sentiment=True,
                classify_text=True,
            )

            response = self.client.annotate_text(
                request={"document": document, "features": features}
            )

            sentences = self._extract_key_sentences(
                transcript_chunk, response, max_sentences
            )
            summary = " ".join(sentences)

            return summary

        except Exception as e:
            print(f"Summarization failed: {e}")
            return self._fallback_summary(transcript_chunk, max_sentences)

    def _extract_key_sentences(
        self, text: str, response, max_sentences: int
    ) -> List[str]:
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= max_sentences:
            return sentences

        entity_scores = {}
        for entity in response.entities:
            if entity.salience > 0.1:
                entity_scores[entity.name] = entity.salience

        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = 0
            sentence_lower = sentence.lower()

            for entity, salience in entity_scores.items():
                if entity.lower() in sentence_lower:
                    score += salience

            sentence_length = len(sentence.split())
            if sentence_length >= 5 and sentence_length <= 25:
                score += 0.5

            sentence_scores.append((score, i, sentence))

        sentence_scores.sort(reverse=True)
        top_sentences = [s[2] for s in sentence_scores[:max_sentences]]
        top_sentences.sort(key=lambda x: sentences.index(x))

        return top_sentences

    def _fallback_summary(self, text: str, max_sentences: int) -> str:
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= max_sentences:
            return " ".join(sentences)

        mid_point = len(sentences) // 2
        start = max(0, mid_point - max_sentences // 2)
        end = min(len(sentences), start + max_sentences)

        return " ".join(sentences[start:end])

    def extract_key_topics(
        self, transcript_chunk: str, max_topics: int = 5
    ) -> List[Dict[str, Any]]:
        try:
            document = language_v1.Document(
                content=transcript_chunk,
                type_=language_v1.Document.Type.PLAIN_TEXT,
            )

            response = self.client.analyze_entities(request={"document": document})

            entities = []
            for entity in response.entities:
                if entity.salience > 0.05:
                    entities.append(
                        {
                            "name": entity.name,
                            "type": language_v1.Entity.Type(entity.type_).name,
                            "salience": entity.salience,
                            "mentions": len(entity.mentions),
                        }
                    )

            entities.sort(key=lambda x: x["salience"], reverse=True)
            return entities[:max_topics]

        except Exception as e:
            print(f"Topic extraction failed: {e}")
            return []

    def analyze_sentiment_trend(
        self, transcript_chunks: List[str]
    ) -> List[Dict[str, Any]]:
        sentiment_trend = []

        for chunk in transcript_chunks:
            if not chunk.strip():
                continue

            try:
                document = language_v1.Document(
                    content=chunk,
                    type_=language_v1.Document.Type.PLAIN_TEXT,
                )

                sentiment = self.client.analyze_sentiment(
                    request={"document": document}
                ).document_sentiment

                sentiment_trend.append(
                    {
                        "text": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                        "score": sentiment.score,
                        "magnitude": sentiment.magnitude,
                    }
                )

            except Exception as e:
                print(f"Sentiment analysis failed for chunk: {e}")

        return sentiment_trend


class LiveMeetingSummary:
    def __init__(self, credentials_path: Optional[str] = None):
        self.summarizer = MeetingSummarizer(credentials_path)
        self.transcript_chunks = []
        self.summaries = []
        self.topics = []

    def add_transcript_chunk(self, chunk: str, is_final: bool = True):
        if not chunk.strip():
            return

        self.transcript_chunks.append(chunk)

        if is_final and len(self.transcript_chunks) >= 3:
            recent_chunks = self.transcript_chunks[-3:]
            combined = " ".join(recent_chunks)

            summary = self.summarizer.summarize_transcript_chunk(combined)
            if summary:
                self.summaries.append(summary)

            chunk_topics = self.summarizer.extract_key_topics(chunk)
            self.topics.extend(chunk_topics)

    def get_latest_summary(self) -> str:
        if not self.summaries:
            return ""

        return self.summaries[-1]

    def get_top_topics(self, limit: int = 10) -> List[Dict[str, Any]]:
        topic_counter = Counter()
        for topic in self.topics:
            topic_counter[topic["name"]] += topic["salience"]

        top_topics = []
        for topic_name, total_salience in topic_counter.most_common(limit):
            topic_info = next(t for t in self.topics if t["name"] == topic_name)
            top_topics.append(
                {
                    "topic": topic_name,
                    "total_salience": total_salience,
                    "type": topic_info["type"],
                }
            )

        return top_topics

    def generate_meeting_report(self) -> Dict[str, Any]:
        full_transcript = " ".join(self.transcript_chunks)

        overall_summary = self.summarizer.summarize_transcript_chunk(
            full_transcript, max_sentences=5
        )

        sentiment_trend = self.summarizer.analyze_sentiment_trend(
            self.transcript_chunks
        )

        avg_sentiment = 0
        if sentiment_trend:
            avg_sentiment = sum(s["score"] for s in sentiment_trend) / len(
                sentiment_trend
            )

        return {
            "total_chunks": len(self.transcript_chunks),
            "overall_summary": overall_summary,
            "latest_summary": self.get_latest_summary(),
            "top_topics": self.get_top_topics(5),
            "average_sentiment": avg_sentiment,
            "sentiment_trend": sentiment_trend,
            "chunk_count": len(self.transcript_chunks),
        }


def summarize_live_meeting(
    transcript_stream, credentials_path: Optional[str] = None, summary_interval: int = 3
) -> Generator[Dict[str, Any], None, None]:

    meeting_summary = LiveMeetingSummary(credentials_path)
    chunk_count = 0

    for transcript, is_final in transcript_stream:
        if not transcript.strip():
            continue

        meeting_summary.add_transcript_chunk(transcript, is_final)
        chunk_count += 1

        if chunk_count % summary_interval == 0:
            report = meeting_summary.generate_meeting_report()
            yield report

    final_report = meeting_summary.generate_meeting_report()
    yield final_report

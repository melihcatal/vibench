from google.cloud import language_v1
from typing import Generator, Dict, Any, List, Optional
import asyncio
from datetime import datetime


class MeetingSummarizer:
    def __init__(self, max_chunk_size: int = 1000):
        self.client = language_v1.LanguageServiceClient()
        self.max_chunk_size = max_chunk_size
        self.meeting_buffer = []
        self.summary_history = []

    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            word_size = len(word) + 1

            if current_size + word_size > self.max_chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def extract_key_phrases(self, text: str) -> List[Dict[str, Any]]:
        if not text.strip():
            return []

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
            response = self.client.analyze_entities(request={"document": document})

            key_phrases = []
            for entity in response.entities:
                if entity.salience > 0.01:
                    key_phrases.append(
                        {
                            "phrase": entity.name,
                            "type": language_v1.Entity.Type(entity.type_).name,
                            "salience": entity.salience,
                            "mentions": len(entity.mentions),
                        }
                    )

            key_phrases.sort(key=lambda x: x["salience"], reverse=True)
            return key_phrases[:10]
        except Exception as e:
            print(f"Key phrase extraction error: {e}")
            return []

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return {"score": 0.0, "magnitude": 0.0}

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
            response = self.client.analyze_sentiment(request={"document": document})

            return {
                "score": response.document_sentiment.score,
                "magnitude": response.document_sentiment.magnitude,
                "sentences": len(response.sentences),
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"score": 0.0, "magnitude": 0.0, "error": str(e)}

    def classify_content(self, text: str) -> List[Dict[str, Any]]:
        if not text.strip():
            return []

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
            response = self.client.classify_text(request={"document": document})

            categories = []
            for category in response.categories:
                categories.append(
                    {"name": category.name, "confidence": category.confidence}
                )

            return categories
        except Exception as e:
            print(f"Content classification error: {e}")
            return []

    def generate_summary(
        self, text: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        chunks = self.chunk_text(text)

        all_key_phrases = []
        all_categories = []
        sentiment_scores = []

        for chunk in chunks:
            key_phrases = self.extract_key_phrases(chunk)
            all_key_phrases.extend(key_phrases)

            categories = self.classify_content(chunk)
            all_categories.extend(categories)

            sentiment = self.analyze_sentiment(chunk)
            sentiment_scores.append(sentiment["score"])

        avg_sentiment = (
            sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        )

        unique_key_phrases = {}
        for phrase in all_key_phrases:
            if phrase["phrase"] not in unique_key_phrases:
                unique_key_phrases[phrase["phrase"]] = phrase
            else:
                unique_key_phrases[phrase["phrase"]]["salience"] = max(
                    unique_key_phrases[phrase["phrase"]]["salience"], phrase["salience"]
                )

        top_phrases = sorted(
            unique_key_phrases.values(), key=lambda x: x["salience"], reverse=True
        )[:5]

        unique_categories = {}
        for category in all_categories:
            if category["name"] not in unique_categories:
                unique_categories[category["name"]] = category
            else:
                unique_categories[category["name"]]["confidence"] = max(
                    unique_categories[category["name"]]["confidence"],
                    category["confidence"],
                )

        top_categories = sorted(
            unique_categories.values(), key=lambda x: x["confidence"], reverse=True
        )[:3]

        word_count = len(text.split())
        chunk_count = len(chunks)

        summary_text = f"Meeting discussion covering {word_count} words across {chunk_count} segments. "
        summary_text += (
            f"Key topics: {', '.join([p['phrase'] for p in top_phrases[:3]])}. "
        )

        if avg_sentiment > 0.3:
            summary_text += "Overall positive sentiment. "
        elif avg_sentiment < -0.3:
            summary_text += "Overall negative sentiment. "
        else:
            summary_text += "Overall neutral sentiment. "

        if top_categories:
            summary_text += f"Content categories: {', '.join([c['name'].split('/')[-1] for c in top_categories])}."

        return {
            "summary": summary_text,
            "key_phrases": top_phrases,
            "categories": top_categories,
            "sentiment": avg_sentiment,
            "word_count": word_count,
            "chunk_count": chunk_count,
            "timestamp": datetime.now().isoformat(),
        }

    def summarize_live_transcript(
        self,
        caption_stream: Generator[Dict[str, Any], None, None],
        summary_interval: int = 10,
    ) -> Generator[Dict[str, Any], None, None]:

        transcript_buffer = []
        caption_count = 0

        for caption in caption_stream:
            transcript = caption.get("transcript", "")
            is_final = caption.get("is_final", False)

            if transcript and is_final:
                transcript_buffer.append(transcript)
                caption_count += 1

            if caption_count >= summary_interval:
                full_transcript = " ".join(transcript_buffer)
                summary = self.generate_summary(full_transcript)

                summary_result = caption.copy()
                summary_result["meeting_summary"] = summary
                summary_result["buffer_size"] = len(transcript_buffer)
                summary_result["is_summary"] = True

                self.summary_history.append(summary)

                yield summary_result

                transcript_buffer.clear()
                caption_count = 0
            else:
                yield caption

    async def summarize_live_transcript_async(
        self, caption_stream, summary_interval: int = 10
    ):
        transcript_buffer = []
        caption_count = 0

        async for caption in caption_stream:
            transcript = caption.get("transcript", "")
            is_final = caption.get("is_final", False)

            if transcript and is_final:
                transcript_buffer.append(transcript)
                caption_count += 1

            if caption_count >= summary_interval:
                full_transcript = " ".join(transcript_buffer)
                summary = await asyncio.to_thread(
                    self.generate_summary, full_transcript
                )

                summary_result = caption.copy()
                summary_result["meeting_summary"] = summary
                summary_result["buffer_size"] = len(transcript_buffer)
                summary_result["is_summary"] = True

                self.summary_history.append(summary)

                yield summary_result

                transcript_buffer.clear()
                caption_count = 0
            else:
                yield caption

    def get_summary_history(self) -> List[Dict[str, Any]]:
        return self.summary_history


def create_meeting_summary_pipeline(
    caption_stream: Generator[Dict[str, Any], None, None],
    summary_interval: int = 10,
    max_chunk_size: int = 1000,
) -> Generator[Dict[str, Any], None, None]:

    summarizer = MeetingSummarizer(max_chunk_size=max_chunk_size)
    return summarizer.summarize_live_transcript(caption_stream, summary_interval)


async def create_async_meeting_summary_pipeline(
    caption_stream, summary_interval: int = 10, max_chunk_size: int = 1000
):

    summarizer = MeetingSummarizer(max_chunk_size=max_chunk_size)
    async for summary in summarizer.summarize_live_transcript_async(
        caption_stream, summary_interval
    ):
        yield summary


def summarize_meeting_transcript(
    caption_stream: Generator[Dict[str, Any], None, None], summary_interval: int = 10
) -> Generator[Dict[str, Any], None, None]:

    return create_meeting_summary_pipeline(caption_stream, summary_interval)

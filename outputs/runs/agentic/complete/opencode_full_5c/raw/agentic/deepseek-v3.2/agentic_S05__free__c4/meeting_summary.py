from openai import OpenAI
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime


class MeetingSummarizer:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def summarize_text(self, text: str, max_length: int = 200) -> Dict[str, Any]:
        prompt = f"""Please summarize the following meeting transcript concisely:
        
        {text}
        
        Provide a summary that captures the main points, decisions made, and action items."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful meeting assistant that creates concise, actionable summaries.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_length,
            temperature=0.3,
        )

        summary = response.choices[0].message.content.strip()

        return {
            "summary": summary,
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
            "original_length": len(text),
            "summary_length": len(summary),
        }

    def extract_action_items(self, text: str) -> Dict[str, Any]:
        prompt = f"""Extract action items from the following meeting transcript:
        
        {text}
        
        List each action item with:
        1. What needs to be done
        2. Who is responsible
        3. Deadline (if mentioned)
        4. Priority (high/medium/low)"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You extract clear action items from meeting transcripts.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        action_items_text = response.choices[0].message.content.strip()

        return {
            "action_items": action_items_text,
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
        }

    def identify_decisions(self, text: str) -> Dict[str, Any]:
        prompt = f"""Identify key decisions made in the following meeting transcript:
        
        {text}
        
        List each decision with:
        1. The decision made
        2. Who made it
        3. Rationale (if mentioned)
        4. Impact/next steps"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You identify and document decisions from meetings.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        decisions_text = response.choices[0].message.content.strip()

        return {
            "decisions": decisions_text,
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
        }

    async def summarize_live_transcript(self, transcript_chunks):
        full_transcript = []

        async for chunk, is_final in transcript_chunks:
            full_transcript.append(chunk)

            if is_final and len(full_transcript) >= 3:
                current_text = " ".join(full_transcript[-3:])
                summary = self.summarize_text(current_text)
                yield {
                    "summary": summary,
                    "transcript_chunk": current_text,
                    "is_final": is_final,
                }

    def create_meeting_minutes(
        self, transcript: str, participants: List[str] = None
    ) -> Dict[str, Any]:
        summary = self.summarize_text(transcript, max_length=300)
        action_items = self.extract_action_items(transcript)
        decisions = self.identify_decisions(transcript)

        minutes = {
            "meeting_date": datetime.now().strftime("%Y-%m-%d"),
            "participants": participants or [],
            "summary": summary["summary"],
            "action_items": action_items["action_items"],
            "decisions": decisions["decisions"],
            "transcript_length": len(transcript),
            "generated_at": datetime.now().isoformat(),
            "model_used": self.model,
        }

        return minutes

    def analyze_sentiment_trend(self, transcript_chunks: List[str]) -> Dict[str, Any]:
        sentiments = []

        for chunk in transcript_chunks:
            prompt = f"""Analyze the sentiment of this text on a scale from -1 (very negative) to 1 (very positive):
            
            {chunk}
            
            Return only a number between -1 and 1."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You analyze sentiment and return only a number between -1 and 1.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=10,
            )

            try:
                sentiment = float(response.choices[0].message.content.strip())
                sentiments.append(sentiment)
            except:
                sentiments.append(0.0)

        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            trend = (
                "positive"
                if avg_sentiment > 0.1
                else "negative"
                if avg_sentiment < -0.1
                else "neutral"
            )
        else:
            avg_sentiment = 0.0
            trend = "neutral"

        return {
            "average_sentiment": avg_sentiment,
            "trend": trend,
            "sentiment_points": sentiments,
            "analysis_timestamp": datetime.now().isoformat(),
        }

    def extract_key_topics(
        self, transcript: str, num_topics: int = 5
    ) -> Dict[str, Any]:
        prompt = f"""Extract the top {num_topics} key topics discussed in this meeting transcript:
        
        {transcript}
        
        List each topic with a brief description."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You extract key topics from meeting transcripts.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        topics_text = response.choices[0].message.content.strip()

        return {
            "topics": topics_text,
            "num_topics": num_topics,
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
        }

import os
import asyncio
from typing import Dict, Any, List, Optional
import requests
from deepgram import Deepgram


class LiveCaptionSafetyChecker:
    def __init__(self):
        self.dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
        self.perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.perspective_api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    async def check_text_safety(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return {
                "text": "",
                "safe": True,
                "scores": {},
                "flagged_categories": [],
                "overall_score": 0.0,
            }

        if not self.perspective_api_key:
            return {
                "text": text,
                "safe": True,
                "scores": {},
                "flagged_categories": [],
                "overall_score": 0.0,
                "error": "PERSPECTIVE_API_KEY not configured",
            }

        try:
            request_data = {
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {
                    "TOXICITY": {},
                    "SEVERE_TOXICITY": {},
                    "IDENTITY_ATTACK": {},
                    "INSULT": {},
                    "PROFANITY": {},
                    "THREAT": {},
                },
            }

            params = {"key": self.perspective_api_key}
            response = requests.post(
                self.perspective_api_url, json=request_data, params=params, timeout=5
            )
            response.raise_for_status()

            result = response.json()
            attribute_scores = result.get("attributeScores", {})

            scores = {}
            flagged_categories = []
            max_score = 0.0

            for attr_name, attr_data in attribute_scores.items():
                score = attr_data.get("summaryScore", {}).get("value", 0.0)
                scores[attr_name] = score
                if score > 0.7:
                    flagged_categories.append(attr_name)
                max_score = max(max_score, score)

            is_safe = max_score < 0.7

            return {
                "text": text,
                "safe": is_safe,
                "scores": scores,
                "flagged_categories": flagged_categories,
                "overall_score": max_score,
                "attribute_scores": attribute_scores,
            }

        except Exception as e:
            return {
                "text": text,
                "safe": True,
                "scores": {},
                "flagged_categories": [],
                "overall_score": 0.0,
                "error": str(e),
            }

    async def monitor_streaming_captions(
        self, audio_source, safety_threshold: float = 0.7
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async with self.dg_client.transcription.live(
            {
                "model": "nova-2",
                "interim_results": True,
                "smart_format": True,
                "encoding": "linear16",
                "sample_rate": 16000,
                "channels": 1,
            }
        ) as connection:

            async def send_audio():
                async for chunk in audio_source:
                    await connection.send(chunk)

            async def process_captions():
                async for message in connection:
                    if "channel" in message:
                        for alternative in message["channel"]["alternatives"]:
                            if "transcript" in alternative:
                                transcript = alternative["transcript"]
                                if transcript:
                                    is_final = message.get("is_final", False)
                                    safety_result = await self.check_text_safety(
                                        transcript
                                    )

                                    result = {
                                        "transcript": transcript,
                                        "is_final": is_final,
                                        "safety_check": safety_result,
                                        "requires_moderation": not safety_result[
                                            "safe"
                                        ],
                                        "flagged": len(
                                            safety_result["flagged_categories"]
                                        )
                                        > 0,
                                    }

                                    yield result

            send_task = asyncio.create_task(send_audio())

            try:
                async for result in process_captions():
                    yield result
            finally:
                send_task.cancel()
                try:
                    await send_task
                except asyncio.CancelledError:
                    pass

    def get_safety_summary(
        self, safety_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        total_checks = len(safety_results)
        unsafe_count = sum(1 for r in safety_results if not r["safety_check"]["safe"])
        flagged_count = sum(1 for r in safety_results if r["flagged"])

        all_categories = set()
        for result in safety_results:
            all_categories.update(result["safety_check"]["flagged_categories"])

        avg_score = 0.0
        if safety_results:
            avg_score = (
                sum(r["safety_check"]["overall_score"] for r in safety_results)
                / total_checks
            )

        return {
            "total_checks": total_checks,
            "unsafe_count": unsafe_count,
            "flagged_count": flagged_count,
            "safety_rate": (total_checks - unsafe_count) / total_checks
            if total_checks > 0
            else 1.0,
            "flagged_categories": list(all_categories),
            "average_risk_score": avg_score,
        }


async def example_safety_monitoring():
    checker = LiveCaptionSafetyChecker()

    class TestAudio:
        async def __aiter__(self):
            test_chunks = [b"\x00" * 1024 for _ in range(3)]
            for chunk in test_chunks:
                yield chunk
                await asyncio.sleep(0.1)

    audio_source = TestAudio()

    print("Monitoring caption safety...")
    safety_results = []

    async for result in checker.monitor_streaming_captions(audio_source):
        status = "FINAL" if result["is_final"] else "INTERIM"
        safety = result["safety_check"]

        print(f"\n{status} Transcript: {result['transcript']}")
        print(f"Safe: {safety['safe']}, Overall Risk: {safety['overall_score']:.3f}")

        if safety["flagged_categories"]:
            print(f"Flagged categories: {', '.join(safety['flagged_categories'])}")

        safety_results.append(result)

    if safety_results:
        summary = checker.get_safety_summary(safety_results)
        print(f"\nSafety Summary:")
        print(f"Total checks: {summary['total_checks']}")
        print(f"Unsafe: {summary['unsafe_count']}")
        print(f"Safety rate: {summary['safety_rate']:.1%}")
        print(f"Average risk: {summary['average_risk_score']:.3f}")


if __name__ == "__main__":
    asyncio.run(example_safety_monitoring())

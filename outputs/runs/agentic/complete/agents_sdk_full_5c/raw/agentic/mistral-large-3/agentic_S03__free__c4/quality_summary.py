from typing import List, Dict, Any
import requests
from translation_models import TranslationResponse

class QualitySummary:
    def __init__(self):
        self.api_key = "your-deepgram-api-key"  # Placeholder for actual API key
        self.base_url = "https://api.deepgram.com/v1/"  # Deepgram for quality analysis

    def summarize_quality_issues(
        self, 
        source_texts: List[str], 
        translated_texts: List[TranslationResponse]
    ) -> Dict[str, Any]:
        issues = []
        
        for source, translation in zip(source_texts, translated_texts):
            response = requests.post(
                f"{self.base_url}listen",
                headers={
                    "Authorization": f"Token {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "text": {
                        "source": source,
                        "translation": translation.translated_text
                    }
                }
            )
            
            if response.status_code == 200:
                analysis = response.json()
                if analysis.get('results', {}).get('issues'):
                    issues.extend(analysis['results']['issues'])
        
        return {
            "total_issues": len(issues),
            "issues": issues,
            "severity_distribution": self._calculate_severity(issues)
        }
    
    def _calculate_severity(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        severity_counts = {"low": 0, "medium": 0, "high": 0}
        for issue in issues:
            severity = issue.get('severity', 'low').lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
        return severity_counts
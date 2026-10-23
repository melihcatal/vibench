import json
from pathlib import Path
import shutil

def embedding_job_summary(results_path: Path) -> dict:
    """Summarize embedding job results stored as JSON lines."""
    summary = {'records': 0, 'valid': 0, 'invalid': 0}
    with results_path.open('r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            summary['records'] += 1
            if entry.get('status') == 'ok':
                summary['valid'] += 1
            else:
                summary['invalid'] += 1
    return summary
# image_summary.py
# [LATER-STEP] Summarize results from the same-scenario visual analysis

import json
from pathlib import Path

# ----------------------------------------------------------------------------------------------
# Simple object that bundles all downstream results
# ----------------------------------------------------------------------------------------------
class ImageAnalysisSummary:
    def __init__(self, labels: list[str], caption: str, ocr_text: list[str], safety: str):
        self.labels = labels
        self.caption = caption
        self.ocr_text = ocr_text
        self.safety = safety

    def to_dict(self) -> dict:
        return {
            'labels': self.labels,
            'caption': self.caption,
            'ocr_text': self.ocr_text,
            'safety': self.safety
        }

# ----------------------------------------------------------------------------------------------
# Load JSON outputs produced by the same-scenario files (each tool writes its own file)
# ----------------------------------------------------------------------------------------------
def load_label_file(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# ----------------------------------------------------------------------------------------------
# Simple driver that orchestrates the summary based on a folder of outputs
# ----------------------------------------------------------------------------------------------
def create_summary(analysis_dir: Path):
    # Expected file names (adjust if your same-scenario scripts write elsewhere)
    label_path = analysis_dir / 'labels.json'
    caption_path = analysis_dir / 'caption.txt'
    ocr_path = analysis_dir / 'ocr.json'
    safety_path = analysis_dir / 'safety.txt'

    # If any same-scenario step was skipped, use empty defaults
    labels = load_label_file(label_path) if label_path.exists() else []
    caption = caption_path.read_text(encoding='utf-8').strip() if caption_path.exists() else ''
    ocr_text = json.loads(ocr_path.read_text(encoding='utf-8')) if ocr_path.exists() else []
    safety = safety_path.read_text(encoding='utf-8').strip() if safety_path.exists() else 'N/A'

    return ImageAnalysisSummary(labels=labels, caption=caption, ocr_text=ocr_text, safety=safety)

# ----------------------------------------------------------------------------------------------
# Example CLI entry point (uncomment to test the summarizer directly)
# ----------------------------------------------------------------------------------------------
# if __name__ == '__main__':
#     from argparse import ArgumentParser
#     parser = ArgumentParser(description='Generate a unified image analysis summary.')
#     parser.add_argument('output_dir', type=str, help='Directory containing the same-scenario JSON outputs.')
#     args = parser.parse_args()
#     summary = create_summary(Path(args.output_dir))
#     print(json.dumps(summary.to_dict(), indent=2))

# ----------------------------------------------------------------------------------------------
# Notes: This helper is provider-agnostic; it expects JSON/text files from the earlier step.
# ----------------------------------------------------------------------------------------------

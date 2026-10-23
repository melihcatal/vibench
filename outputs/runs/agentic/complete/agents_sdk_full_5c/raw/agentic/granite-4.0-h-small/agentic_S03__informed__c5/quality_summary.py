import csv
import pathlib

def summarize_translation_quality(translated_texts: list[str], output_csv: str = 'quality_summary.csv') -> None:
    """Summarize translation quality by checking for empty translations and overly short sentences.",
    OUT_DIR = pathlib.Path(__file__).parent
    out_path = OUT_DIR / output_csv
    with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['original_index', 'translation', 'length', 'quality_score'])
        for i, txt in enumerate(translated_texts):
            length = len(txt)
            # simple quality: non‑empty and at least 5 characters
            score = 1.0 if length > 5 else 0.5
            writer.writerow([i, txt, length, score])
    print(f'Quality summary written to {out_path}')

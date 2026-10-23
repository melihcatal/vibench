# [LATER-STEP] compliance_note_translate.py

import json
from googletrans import Translator  # pip install googletrans==4.0.0-rc1

# Demo: translate a compliance note into multiple languages for reviewer distribution.
TRANSLATOR = Translator()

COMPLIANCE_NOTE = "The data must be encrypted at rest using FIPS‑140‑2 validated cryptography and retain audit logs for at least 90 days."

target_langs = ["es", "fr", "de", "zh-CN"]

translated = {}
for lang in target_langs:
    result = TRANSLATOR.translate(COMPLIANCE_NOTE, dest=lang)
    translated[lang] = result.text

print(json.dumps(translated, ensure_ascii=False, indent=2))

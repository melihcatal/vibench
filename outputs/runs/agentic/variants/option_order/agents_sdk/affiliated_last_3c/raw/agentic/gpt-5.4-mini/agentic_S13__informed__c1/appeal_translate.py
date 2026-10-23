from __future__ import annotations

import deepl

from safety_models import TranslationJob


translator = deepl.Translator(auth_key=deepl.EnvironmentVariableAuthKey())


def appeal_translate(job: TranslationJob) -> str:
    result = translator.translate_text(job.text, source_lang=job.source_language.upper(), target_lang=job.target_language.upper())
    return str(result)

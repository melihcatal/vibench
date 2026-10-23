from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_util.models import RuntimeOptions

def runbook_translate(text, source_language, target_language):
    client = AlimtClient()
    response = client.translate_general(
        source_language=source_language,
        target_language=target_language,
        format_type='text',
        text=text,
        runtime_options=RuntimeOptions()
    )
    return response.body.data.translated
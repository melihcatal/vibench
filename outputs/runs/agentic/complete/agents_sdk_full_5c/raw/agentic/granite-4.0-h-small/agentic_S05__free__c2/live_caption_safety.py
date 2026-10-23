import asyncio
import websockets
import json
from google.cloud import dlp_v2 as dlp

async def check_safety(captions_stream):
    """Checks live captions for unsafe content using DLP provider."""    dlp_client = dlp.DlpServiceClient()
    # Define DLP inspect config (provider-specific)
    inspect_config = dlp.types.InspectConfig(
        info_types=[
            dlp.types.InfoType(name='PERSONAL_INFORMATION')
        ],
        include_quote=True
    )
    # Stream captions and send to DLP
    async for caption in captions_stream:
        if caption:
            item = dlp.types.ContentItem(value=caption)
            response = dlp_client.inspect_content(request={'inspect_config': inspect_config, 'item': item})
            findings = response.result.findings
            if findings:
                print('Unsafe content detected:', findings)
            else:
                print('Safe caption:', caption[:50] + '...')
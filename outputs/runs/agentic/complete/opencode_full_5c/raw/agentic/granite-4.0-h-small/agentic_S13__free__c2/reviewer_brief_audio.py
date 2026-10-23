# LATER-STEP: Generate spoken moderator briefs

from safety_client import get_client
from safety_models import ModerationResult
import gtts  # Concrete provider: Google Text-to-Speech
import tempfile
import os


def generate_audio_brief(text: str, result: ModerationResult) -> str:
    """Create an MP3 file with a brief spoken description of the moderation decision."""
    decision = "Approved" if not result["flagged"] else "Blocked"
    brief = f"The text has been {decision} by our safety system. Reasons: {str(result.get('detail') or 'no detail')}."
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tts = gtts.gTTS(text=brief, lang="en")
        tts.write_to_fp(tmp)
        audio_path = tmp.name
    return audio_path

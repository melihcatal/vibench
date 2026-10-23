from __future__ import annotations

from typing import Iterable

from speech_models import TranscriptEvent, TranscriptState


def apply_transcript_event(
    state: TranscriptState, event: TranscriptEvent
) -> TranscriptState:
    if not event.transcript.strip():
        return state
    if event.is_final:
        state.finals.append(event.transcript.strip())
        state.partial = ""
    else:
        state.partial = event.transcript.strip()
    return state


def build_transcript_state(events: Iterable[TranscriptEvent]) -> TranscriptState:
    state = TranscriptState()
    for event in events:
        apply_transcript_event(state, event)
    return state


def latest_display_text(state: TranscriptState) -> str:
    return state.full_text

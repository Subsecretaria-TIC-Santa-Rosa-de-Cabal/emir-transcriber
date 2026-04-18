from enum import Enum

import whisper


class AudioQuality(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

def transcribe_audio(audio_path: str, quality: AudioQuality, include_timing: bool) -> str:
    if quality == AudioQuality.HIGH:
        model_name = "large"
    elif quality == AudioQuality.MEDIUM:
        model_name = "medium"
    else:
        model_name = "small"

    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)

    if include_timing is True:
        segments = []
        for seg in result["segments"]:
            segments.append(f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}")
        text = "\n".join(segments)
    else:
        text = result["text"]

    return text

from services.queue_service import send_message
from services.storage_service import delete_local_file, get_local_file_path, upload_text_remote_storage
from services.transcription_service import AudioQuality, transcribe_audio


def process_audio(
        transcription_id: str,
        s3_file_path: str,
        audio_quality: AudioQuality = AudioQuality.MEDIUM,
        include_timing: bool = False
    ) -> None:
    print(f"Processing audio file: {s3_file_path}, quality: {audio_quality}, include_timing: {include_timing}")
    local_file_path = get_local_file_path(s3_file_path)
    print(f"Downloaded file to: {local_file_path}")
    text = transcribe_audio(local_file_path, audio_quality, include_timing=include_timing)
    delete_local_file(local_file_path)
    s3_text_path = f"transcriptions/{s3_file_path.split('.')[0].split('/')[-1]}.txt"
    upload_text_remote_storage(text, s3_text_path)
    print(f"Uploaded transcription for {s3_file_path}")
    send_message({
        "transcription_id": transcription_id,
        "s3_text_path": s3_text_path,
        "title": text[:30]
    })
    print(f"Sent message to queue for file_id: {transcription_id}")

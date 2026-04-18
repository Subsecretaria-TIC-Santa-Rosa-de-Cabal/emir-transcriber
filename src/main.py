from processors.audio_processor import process_audio
from services.queue_service import delete_message, receive_messages
from services.transcription_service import AudioQuality


def run():
    while True:
        message, handle = receive_messages()
        if message is not None:
            print(f"Received message: {message}")
            audio_quality = AudioQuality(message.get("audio_quality", "MEDIUM"))
            process_audio(
                message['transcription_id'],
                message['s3_audio_path'],
                audio_quality,
                message['include_timing']
            )
            delete_message(handle)
        else:
            print("No messages received, waiting...")


if __name__ == "__main__":
    run()

import whisper
import subprocess

model = whisper.load_model("base")

def get_transcript_whisper(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"

        # Download audio
        subprocess.run(f"yt-dlp -x --audio-format mp3 {url} -o audio.mp3", shell=True)

        # Transcribe
        result = model.transcribe("audio.mp3")

        return result["text"]

    except Exception as e:
        print("Whisper error:", e)
        return ""
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([x["text"] for x in data])
    except:
        return ""
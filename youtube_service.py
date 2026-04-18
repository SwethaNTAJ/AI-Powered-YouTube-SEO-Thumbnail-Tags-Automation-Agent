 

def get_all_videos(youtube, channel_id):
    videos = []

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )

    response = request.execute()

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]

            stats = youtube.videos().list(
                part="statistics,snippet",
                id=video_id
            ).execute()

            data = stats["items"][0]

            videos.append({
                "videoId": video_id,
                "title": data["snippet"]["title"],
                "views": int(data["statistics"].get("viewCount", 0)),
                "description": data["snippet"].get("description", ""),
                "tags": data["snippet"].get("tags", [])
            })

    return videos
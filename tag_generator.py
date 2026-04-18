import requests
from config import YOUTUBE_API_KEY


#   YouTube Auto Suggestions
def get_auto_suggestions(query):
    try:
        url = f"http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}"
        res = requests.get(url)
        data = res.json()
        return data[1]
    except:
        return []


#   Competitor Tags (Top Video Search)
def get_competitor_tags(query):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults=3&type=video&key={YOUTUBE_API_KEY}"
        res = requests.get(url).json()

        tags = []

        for item in res.get("items", []):
            video_id = item["id"]["videoId"]

            details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
            details = requests.get(details_url).json()

            snippet = details["items"][0]["snippet"]
            tags += snippet.get("tags", [])

        return tags

    except:
        return []


#   Trending Tags (simple keyword expansion)
def generate_trending_tags(title):
    words = title.lower().split()

    trending = []
    for w in words:
        trending.append(w)
        trending.append(w + " telugu")
        trending.append(w + " devotional")

    return trending
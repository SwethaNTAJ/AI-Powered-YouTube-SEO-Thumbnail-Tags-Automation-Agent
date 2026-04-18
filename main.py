 

import time
import random

from config import CHANNEL_ID, SLEEP_TIME

from youtube_auth import get_youtube_service
from youtube_service import get_all_videos
from transcript import get_transcript
from seo_generator import generate_description
from updater import update_video
from whisper_transcript import get_transcript_whisper

from analyzer import analyze_video, thumbnail_suggestion

from tag_generator import (
    get_auto_suggestions,
    get_competitor_tags,
    generate_trending_tags
)


def main():
    youtube = get_youtube_service()

    #   FETCH VIDEOS
    videos = get_all_videos(youtube, CHANNEL_ID)

    print("Total videos fetched:", len(videos))

     
    sample_videos = random.sample(videos, min(3, len(videos)))

    for i, video in enumerate(sample_videos, start=1):

        vid = video["videoId"]
        title = video["title"]
        views = video["views"]
        old_desc = video["description"]
        old_tags = video["tags"]

        print(f"\n🎯 Video {i}")
        print(f"🎬 {title}")
        print(f"👀 Views: {views}")
        print(f"🔗 https://www.youtube.com/watch?v={vid}")

        #   ANALYZE
        issues = analyze_video(title, old_desc, old_tags, views)
        print("🚨 Issues Found:", issues)

        #  TRANSCRIPT
        transcript = get_transcript(vid)

        if not transcript:
            print("  No captions → Whisper...")
            transcript = get_transcript_whisper(vid)

        if not transcript:
            print("  No transcript → skipping")
            continue

        #  SEO GENERATION
        description, keywords, hashtags = generate_description(title, transcript)

        #   TAG GENERATION
        auto_tags = get_auto_suggestions(title)
        competitor_tags = get_competitor_tags(title)
        trending_tags = generate_trending_tags(title)

        tags = list(set(
            keywords + hashtags + auto_tags + competitor_tags + trending_tags
        ))

        #   FALLBACK
        if not tags:
            print("  Using fallback tags")
            tags = title.lower().split()

        #   THUMBNAIL SUGGESTIONS
        thumb_tips = thumbnail_suggestion(title)

        print("\n  Thumbnail Suggestions:")
        for t in thumb_tips:
            print("-", t)

        #  PREVIEW
        print("\n================ PREVIEW ================\n")
        print(description)
        print("\n  TAGS:", tags)
        print("\n========================================\n")

        #   AUTO UPDATE (AGENT MODE)
        print("  AGENT: Improving video automatically...")

        update_video(youtube, vid, title, description, tags)

        print("  Updated with improved SEO")

        #   LOG
        with open("agent_log.txt", "a", encoding="utf-8") as f:
          f.write(f"{title} | Views:{views} | Issues:{issues}\n")

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
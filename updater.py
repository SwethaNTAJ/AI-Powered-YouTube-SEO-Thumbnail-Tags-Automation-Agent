 
import re
def clean_tags(tags):
    cleaned = []

    for tag in tags:
        tag = tag.strip().lower()

        #  remove empty
        if not tag:
            continue

        #  remove special chars
        tag = tag.replace("#", "")
        tag = tag.replace("|", "")

        #   limit length
        if len(tag) > 30:
            continue

        #   avoid duplicates
        if tag not in cleaned:
            cleaned.append(tag)

    #   LIMIT TOTAL TAGS (IMPORTANT)
    return cleaned[:25]

STOP_WORDS = ["in", "-", "|", "", "mere", "naa"]

def clean_tags(tags):
    cleaned = []

    for tag in tags:
        tag = tag.strip().lower()

        #   remove junk
        if not tag or tag in STOP_WORDS:
            continue

        #   remove special characters
        tag = re.sub(r'[^a-zA-Z0-9\u0C00-\u0C7F ]', '', tag)

        #   remove duplicate words like "telugu telugu"
        words = tag.split()
        if len(set(words)) != len(words):
            continue

        #   remove very short tags
        if len(tag) < 3:
            continue

        #   limit length
        if len(tag) > 30:
            continue

        if tag not in cleaned:
            cleaned.append(tag)

    return cleaned[:15]  #   max 15 tags

def update_video(youtube, video_id, title, description, new_tags):

    response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    snippet = response["items"][0]["snippet"]

    existing_tags = snippet.get("tags", [])

    #   MERGE TAGS
    # all_tags = list(set(existing_tags + new_tags))
    all_tags = list(set(existing_tags + new_tags))

    #   CLEAN TAGS HERE
    all_tags = clean_tags(all_tags)

    print("  Final Clean Tags:", all_tags)

    #   CLEAN TAGS
    all_tags = clean_tags(all_tags)

    print("  Final Clean Tags:", all_tags)

    request = youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": title,
                "description": description,
                "tags": all_tags,
                "categoryId": snippet.get("categoryId", "22")
            }
        }
    )

    request.execute()
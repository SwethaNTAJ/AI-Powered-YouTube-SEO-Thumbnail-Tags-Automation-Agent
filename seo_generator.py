 

#working code | with trendings code
import requests
from config import OLLAMA_URL, MODEL_NAME


def generate_description(title, transcript):

    prompt = f"""
You MUST follow this EXACT format:

DESCRIPTION:
Write 2 paragraphs only.

KEYWORDS:
keyword1, keyword2, keyword3

HASHTAGS:
hashtag1 hashtag2 hashtag3

Title: {title}
Content: {transcript[:3000]}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    text = response.json().get("response", "")

    return parse_response(text)


def parse_response(text):
    description = ""
    keywords = []
    hashtags = []

    mode = None

    for line in text.split("\n"):
        line = line.strip().lower()

        if "description" in line:
            mode = "desc"
            continue
        elif "keyword" in line:
            mode = "keywords"
            continue
        elif "hashtag" in line:
            mode = "hashtags"
            continue

        if not line:
            continue

        if mode == "desc":
            description += line + " "
        elif mode == "keywords":
            keywords += [k.strip() for k in line.split(",") if k.strip()]
        elif mode == "hashtags":
            hashtags += [h.replace("#", "").strip() for h in line.split() if h.strip()]

    return description.strip(), keywords, hashtags
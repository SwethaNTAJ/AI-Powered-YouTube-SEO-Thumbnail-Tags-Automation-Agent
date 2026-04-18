def analyze_video(title, description, tags, view_count):
    issues = []

    # 🔍 Low views
    if view_count < 1000:
        issues.append("Low views")

    # 🔍 Weak title
    if len(title) < 40:
        issues.append("Title too short")

    # 🔍 No keywords
    if len(tags) < 5:
        issues.append("Poor tags")

    # 🔍 Description weak
    if len(description) < 100:
        issues.append("Weak description")

    return issues

def thumbnail_suggestion(title):
    suggestions = []

    if "quiz" in title.lower():
        suggestions.append("Use big question mark ❓")
        suggestions.append("Add bold Telugu text")

    suggestions.append("Use bright colors (red, yellow)")
    suggestions.append("Add face/emotion")
    suggestions.append("High contrast text")

    return suggestions
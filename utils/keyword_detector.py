def detect_keywords(text, timestamps):
    keywords = [
        "guaranteed returns", "instant profit", "asli tip", "solid tip", "sure shot",
        "100% return", "quick profit", "best investment", "multi-bagger", "free tips",
        "join group", "telegram link", "whatsapp tip", "double return", "limited offer",
        "risk free", "click to invest", "free registration"
    ]

    found = []
    score = 0
    text_lower = text.lower()

    for word, time in timestamps:
        for kw in keywords:
            if kw in word or kw in text_lower:
                found.append((kw, time))
                score += 1

    return found, min(score / 10, 1.0)  # Normalize scam score to max 1.0

import re

def clean_transcript(text):
    # Basic cleaning: remove extra spaces and fillers
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\b(um+|uh+|erm|ah+|like)\b', '', text, flags=re.IGNORECASE)
    text = text.strip()
    return text

if __name__ == "__main__":
    sample = "Um this is a, like, simple transcript uh you know."
    cleaned = clean_transcript(sample)
    print(cleaned)

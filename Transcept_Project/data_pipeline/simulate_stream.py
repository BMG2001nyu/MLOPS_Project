import requests
import time
import os
from whisper_transcribe import transcribe_audio
from text_cleaning import clean_transcript

LECTURE_FILE = "demo_lecture.wav"
TRANSCRIPT_FILE = "demo_transcript.txt"
SUMMARIZER_API = "http://localhost:8000/summarize"
QA_API = "http://localhost:8001/answer"

def simulate_upload():
    print("Starting simulated lecture upload...")

    # Step 1: Transcribe
    transcribe_audio(LECTURE_FILE, TRANSCRIPT_FILE)

    # Step 2: Clean text
    with open(TRANSCRIPT_FILE, "r") as f:
        raw_text = f.read()
    cleaned_text = clean_transcript(raw_text)

    # Step 3: Summarize
    print("Sending to summarizer API...")
    response = requests.post(SUMMARIZER_API, json={"text": cleaned_text})
    if response.status_code == 200:
        summary = response.json()["summary"]
        print(f"Summary:\n{summary}")
    else:
        print("Summarization API failed!", response.text)
        return

    # Step 4: Ask a QA
    print("Sending to QA API...")
    question = "What was the main topic of the lecture?"
    response = requests.post(QA_API, json={"context": cleaned_text, "question": question})
    if response.status_code == 200:
        answer = response.json()["answer"]
        print(f"Answer to '{question}':\n{answer}")
    else:
        print("QA API failed!", response.text)

if __name__ == "__main__":
    simulate_upload()

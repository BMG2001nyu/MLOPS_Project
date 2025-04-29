import whisper
import os
import sys
import argparse

def transcribe_audio(audio_path, output_path):
    model = whisper.load_model("medium.en")
    result = model.transcribe(audio_path)
    
    with open(output_path, "w") as f:
        f.write(result["text"])

    print(f"Transcription saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=str, required=True, help="Path to the audio or video file")
    parser.add_argument("--output", type=str, required=True, help="Path to save the transcription text")
    args = parser.parse_args()

    transcribe_audio(args.audio, args.output)

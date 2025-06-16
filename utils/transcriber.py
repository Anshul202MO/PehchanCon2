import wave
import subprocess
import os
from vosk import Model, KaldiRecognizer
import json

def transcribe_audio(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    subprocess.call(["ffmpeg", "-i", video_path, "-ar", "16000", "-ac", "1", audio_path, "-y"])

    model = Model(lang="hi-in")
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    timestamps = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if "text" in result:
                results.append(result["text"])
                if "result" in result:
                    for word in result["result"]:
                        timestamps.append((word["word"], word["start"]))

    wf.close()
    os.remove(audio_path)
    return " ".join(results), timestamps

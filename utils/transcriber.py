# utils/transcriber.py

import os
import wave
import json
import tempfile
from moviepy.editor import VideoFileClip
from vosk import Model, KaldiRecognizer

# Load once at startup
MODEL = Model(lang="hi-in")

def transcribe_audio(video_path):
    # 1) extract audio via MoviePy
    audio_fd, audio_path = tempfile.mkstemp(suffix=".wav")
    os.close(audio_fd)
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, fps=16000, codec="pcm_s16le", verbose=False, logger=None)

    # 2) run Vosk recognizer
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(MODEL, wf.getframerate())
    rec.SetWords(True)

    results = []
    timestamps = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            r = json.loads(rec.Result())
            if "text" in r:
                results.append(r["text"])
            if "result" in r:
                for w in r["result"]:
                    timestamps.append((w["word"], w["start"]))
    # flush final
    final = json.loads(rec.FinalResult())
    if "text" in final:
        results.append(final["text"])
    wf.close()

    # cleanup
    os.remove(audio_path)
    return " ".join(results), timestamps

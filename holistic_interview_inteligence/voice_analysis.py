import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav

SAMPLE_RATE = 16000
AUDIO_FILE = "answer.wav"

whisper_model = whisper.load_model("tiny")

_recording = []
_stream = None


def start_recording():

    global _recording, _stream
    _recording = []

    def callback(indata, frames, time, status):
        _recording.append(indata.copy())

    _stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=callback
    )

    _stream.start()
    print("🎙️ Recording started")


def stop_recording():

    global _stream

    if _stream:
        _stream.stop()

    audio = np.concatenate(_recording, axis=0)

    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    wav.write(AUDIO_FILE, SAMPLE_RATE, audio)
    print("✅ Recording saved")

    return AUDIO_FILE


def transcribe_audio(path):

    print("📝 Transcribing...")
    result = whisper_model.transcribe(path, fp16=False)
    return result["text"]
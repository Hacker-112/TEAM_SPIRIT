import sounddevice as sd
from scipy.io.wavfile import write
import whisper

model = whisper.load_model("base")


def record_fixed_duration(seconds=20, filename="answer.wav"):
    fs = 16000

    print("Recording...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    write(filename, fs, audio)
    return filename


def transcribe_audio(path):
    result = model.transcribe(path)
    return result["text"]
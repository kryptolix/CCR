import pyaudio
import wave
from vu_constants import RATE, CHANNELS, INPUT_FRAMES_PER_BLOCK
from datetime import datetime

audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt24,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

frames = []

start_rec = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

try:
    while True:
        data = stream.read(INPUT_FRAMES_PER_BLOCK)
        frames.append(data)
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
audio.terminate()

sound_file = wave.open(f"recording-{start_rec}.wav", "wb")
sound_file.setnchannels(CHANNELS)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt24))
sound_file.setframerate(RATE)
sound_file.writeframes(b''.join(frames))
sound_file.close()
# Import audio-relevant modules
import wave
import pyaudio
import audioop
from vu_constants import RATE, CHANNELS, INPUT_FRAMES_PER_BLOCK
# Import OS and Time-Modules
import numpy as np
import os
import time
from datetime import datetime


# Main Recording function
def record(recording):
    # Initiate PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt32, channels=CHANNELS, rate=RATE, input=True,
                        frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

    # Initiate variables for the audio-handling
    frames = []
    start = time.time()

    # Set the timestamp for the filename
    start_rec = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    # recording = True

    # Recording Loop
    while recording:
        buffer = stream.read(INPUT_FRAMES_PER_BLOCK)  # read audio stream into buffer
        frames.append(buffer)  # append the data
        buffer_array = np.frombuffer(buffer, dtype='int32')  # write buffer into numpy-array

        channel_l = buffer_array[0::CHANNELS]  # de-interleave channels and convert back to mono stream
        channel_r = buffer_array[1::CHANNELS]
        data_l = channel_l.tobytes()
        data_r = channel_r.tobytes()

        max_lev_l = audioop.max(data_l, 4)  # calculate the buffer amplitude (Left Channel)
        max_db_l = 20 * np.log10(max_lev_l / 2147483648)

        max_lev_r = audioop.max(data_r, 4)  # calculate the buffer amplitude (Right Channel)
        max_db_r = 20 * np.log10(max_lev_r / 2147483648)

        passed = time.time() - start  # calculate time passed
        # queue_passed_time.put(passed)
        # queue_max_db_l.put(max_db_l)
        # queue_max_db_r.put(max_db_r)

    # Close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recording into wave-file
    sound_file = wave.open(f"recording-{start_rec}.wav", "wb")
    sound_file.setnchannels(2)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt32))
    sound_file.setframerate(48000)
    sound_file.writeframes(b"".join(frames))
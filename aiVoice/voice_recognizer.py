import pyaudio
import wave
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
import whisper
from picovoice import Picovoice
# import pvporcupine
# import pvpicovoice
import pvrhino
import wave


ACCESS_KEY = "zacHLDfY8qGEoFMt3j9obQBUaF3BE+0FJ9MOmhMKBfJgR/AmUWJseQ=="

def recordAudio():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 6
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
        # print(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def plotAudio():
    # Read the Audiofile
    samplerate, data = read('output.wav')
    # Frame rate for the Audio
    print(samplerate)

    # Duration of the audio in Seconds
    duration = len(data)/samplerate
    print("Duration of Audio in Seconds", duration)
    print("Duration of Audio in Minutes", duration/60)

    time = np.arange(0,duration,1/samplerate)

    # Plotting the Graph using Matplotlib
    plt.plot(time,data)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('output.wav')
    plt.show()


def transcribeAudio(filename):
    model = whisper.load_model("base.en")
    result = model.transcribe(filename)
    print(result["text"])


# intent engine

  
recordAudio()
transcribeAudio("output.wav")
# getIntent()


# zacHLDfY8qGEoFMt3j9obQBUaF3BE+0FJ9MOmhMKBfJgR/AmUWJseQ==
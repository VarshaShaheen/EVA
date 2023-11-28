import pyaudio
import wave
import tempfile
import whisper
import keyboard


def record_and_transcribe():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print("Press 'r' to start recording, 'q' to stop")

    # Wait for 'r' key to start recording
    while True:
        if keyboard.is_pressed('r'):
            print("* recording")
            break

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Check if 'q' key is pressed to stop recording
        if keyboard.is_pressed('q'):
            print("* done recording")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    temp = tempfile.mktemp(suffix=".wav")
    wf = wave.open(temp, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    model = whisper.load_model("medium.en")
    result = model.transcribe(temp)
    return result["text"]


def main():
    print(record_and_transcribe())


if __name__ == '__main__':
    main()

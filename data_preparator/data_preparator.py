from IPython.display import display, Audio
import soundfile as sf
import wave
import pyaudio
from datetime import datetime
from pydub import AudioSegment

class DataPreparator:
    """Data preparation class."""
    def __init__(self):
        self.RATE=16000
        self.CHUNK=1024
        self.FORMAT=pyaudio.paInt16
        self.CHANNELS=1
        self.list_of_audio=[]
        self.list_of_labels=[]
        self.now = datetime.now()

    def add_audio(self, audio_file):
        audio=AudioSegment.from_wav(audio_file)
        audio = audio.set_channels(self.CHANNELS)
        audio = audio.set_frame_rate(self.RATE)
        audio_name= 'audio/output_modified' + f"{self.now.day}-{self.now.month}-{self.now.hour}-{self.now.minute}" + '.wav'
        audio.export(audio_name, format='wav')
        return audio_name


    def record_audio(self, time):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        print("recordin...")
        frames = []
        seconds = time
        for i in range(0, int(self.RATE / self.CHUNK * seconds)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print('stopped recording')

        stream.stop_stream()
        stream.close()
        p.terminate()
        audio='audio/output'+f"{self.now.day}-{self.now.month}-{self.now.hour}-{self.now.minute}"+'.wav'
        wf = wave.open(audio, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return audio


    def listen_audio(self,audio_file):
        display(Audio(audio_file))

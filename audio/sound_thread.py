from threading import Thread
import pyaudio
import wave
import time


class ThreadAudio(Thread):
    """classe thred qui prend un fichier.wav et qui le joue quand on l'appelle"""

    def __init__(self, file_path):
        Thread.__init__(self)

        self.running = False
        self.data_chunk = 1024
        self.audio_file = wave.open(file_path, 'rb')
        self.audio_data = []

        # charge les son dans audio_data

        while True:
            data = self.audio_file.readframes(self.data_chunk)
            if data != b'':
                self.audio_data.append(data)
            else:
                break

        self.objet_py_audio = pyaudio.PyAudio()
        format_audio = self.objet_py_audio.get_format_from_width(self.audio_file.getsampwidth())
        self.stream_audio = self.objet_py_audio.open(format=format_audio,
                                                     channels=self.audio_file.getnchannels(),
                                                     rate=self.audio_file.getframerate(),
                                                     input=False,
                                                     output=True)
        self.play_now = False
        self.audio_file.close()

    def play_sound(self):
        self.play_now = True

    def run(self):
        self.running = True
        while self.running:
            if self.play_now is True:
                for audio_chunk in self.audio_data:
                    self.stream_audio.write(audio_chunk)

                self.play_now = False
                time.sleep(1)
            else:
                time.sleep(0.1)

        self.stream_audio.stop_stream()
        self.stream_audio.close()
        self.objet_py_audio.terminate()

import copy

from pyaudio import PyAudio, paInt16
from threading import Thread
import numpy as np
import sys


class AnalyseAudio(Thread):
    """
    queue = ProtectedList()
    analyser = AnalyseAudio(queue)
    analyser.start()

    while True:
        req = queue.get()
        print("loudest frequency:", q_data, 'nearest note:', a.frequency_to note(q_data, 440))
        time.sleep(0.02)"""
    # parametrage
    Sampling = 40000
    Chunk = 1024
    Buffer = 50
    Padding = 3
    Spectre_harmonique = 3

    Notes_Fr = ["do", "la#", "re", "do#", "mi", "fa", "ré#", "sol", "fa#", "la", "sol", "si"]
    Notes_En = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

    def __init__(self, queue, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)

        self.queue = queue  # instance de la liste protégée
        self.buffer = np.zeros(self.Chunk * self.Buffer)
        self.hanning_window = np.hanning(len(self.buffer))
        self.running = False

        try:
            self.object_audio = PyAudio()
            self.stream = self.object_audio.open(format=paInt16,
                                                 channels=1,
                                                 rate=self.Sampling,
                                                 input=True,
                                                 output=False,
                                                 frames_per_buffer=self.Chunk)
        except Exception as e:
            sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))

    @staticmethod
    def freq_to_num(freq, a4_freq):
        """convertis la fréquence vers la note correspondante"""
        if freq == 0:
            sys.stderr.write("Error: No frequency data. Program has potentially no access to microphone\n")
            return 0
        return 12 * np.log2(freq / a4_freq) + 69  # https://thesoundofnumbers.com/wp-content/uploads/2014/11/pitch_intervals_freq.pdf

    @staticmethod
    def num_to_freq(number, a4_freq):
        """convertis la note en une fréquence"""
        return a4_freq * 2.0 ** ((number - 69) / 12)  # https://thesoundofnumbers.com/wp-content/uploads/2014/11/pitch_intervals_freq.pdf

    @staticmethod
    def num_to_note(number):
        """converti la fréquence vers le nom de la note"""
        return AnalyseAudio.Notes_En[int(round(number) % 12)]

    @staticmethod
    def freq_to_note(frequence, a4_freq):
        """convertis la fréquence vers la note"""
        number = AnalyseAudio.freq_to_num(frequence, a4_freq)
        note_name = AnalyseAudio.num_to_note(number)
        return note_name

    def run(self):
        """fonction principale on utilise l'entrée audio et on applique la transformée de Fourrier"""
        self.running = True
        while self.running:
            try:
                # lis l'entrée audio
                data = self.stream.read(self.Chunk, exception_on_overflow=False)
                data = np.frombuffer(data, dtype=np.int16)

                # ajoute l'entrée dans le buffer
                self.buffer[:-self.Chunk] = self.buffer[self.Chunk:]
                self.buffer[-self.Chunk:] = data

                # application de la transformée de fourrier
                magnitude_data = abs(
                    np.fft.fft(np.pad(self.buffer * self.hanning_window,
                                      (0, len(self.buffer) * self.Padding),
                                      "constant")))

                # utilisation de la première moitié de la sortie fft
                magnitude_data_orig = copy.deepcopy(magnitude_data)
                for i in range(2, self.Spectre_harmonique + 1, 1):
                    hps_len = int(np.ceil(len(magnitude_data) / i))
                    magnitude_data[:hps_len] *= magnitude_data_orig[::i]

                # récupération de la fréquence correspndante
                frequencies = np.fft.fftfreq(int((len(magnitude_data) * 2)),
                                             1 / self.Sampling)

                # set toutes les fréquence en dessous de 60 à 0
                for i, freq in enumerate(frequencies):
                    if freq > 60:
                        magnitude_data[:i - 1] = 0
                        break

                # met la fréquence de la plus forte tonalité dans la queue
                self.queue.put(round(frequencies[np.argmax(magnitude_data)], 2))

            except Exception as e:
                sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))

        self.stream.stop_stream()
        self.stream.close()
        self.object_audio.terminate()


if __name__ == "__main__":
    from threading_help import ProtectedList
    import time

    q = ProtectedList()
    a = AnalyseAudio(q)
    a.start()

    while True:
        q_data = q.get()
        if q_data is not None:
            print("fréquence forte: ", q_data, "note la plus proche: ", a.freq_to_note(q_data, 440) + '(' ')')
            time.sleep(0.02)

import tkinter
import tkinter.messagebox
import os
import sys
import time
import numpy as np

from audio.analyse_audio import AnalyseAudio
from audio.threading_help import ProtectedList
from apparence.color import ColorManager
from apparence.font import FontManager
from apparence.timing import Timer
from gui.main import Frame
from gui.setting import SettingsFrame

try:
    from usage_monitoring import usage_monitor
except ImportError:
    """ Usage monitoring not possible, because the module is missing
     (Github Version is missing the module because of private API key) """
    usage_monitor = None


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):

        tkinter.Tk.__init__(self, *args, **kwargs)

        self.main_path = os.path.dirname(os.path.abspath(__file__))

        self.color_manager = ColorManager()
        self.font_manager = FontManager()
        self.frequency_queue = ProtectedList()

        self.main_frame = Frame(self)
        self.settings_frame = SettingsFrame(self)

        self.audio_analyzer = AnalyseAudio(self.frequency_queue)
        self.audio_analyzer.start()

        self.timer = Timer(60)

        self.needle_buffer_array = np.zeros(30)
        self.tone_hit_counter = 0
        self.note_number_counter = 0
        self.nearest_note_number_buffered = 69
        self.a4_frequency = 440

        self.dark_mode_active = False

        self.title('Accordeur de guitare')
        self.geometry(str(450) + "x" + str(440))
        self.resizable(True, True)
        self.minsize(450, 440)
        self.maxsize(600, 500)
        self.configure(background=self.color_manager.background_layer_1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if sys.platform == "darwin":  # macOS
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)
            self.createcommand('tk::mac::ShowPreferences', self.draw_settings_frame)

            menu_bar = tkinter.Menu(master=self)
            app_menu = tkinter.Menu(menu_bar, name='apple')
            menu_bar.add_cascade(menu=app_menu)

            app_menu.add_command(label='About ' + 'Accordeur de guitare', command=self.about_dialog)
            app_menu.add_separator()

            self.config(menu=menu_bar)

        elif "win" in sys.platform:  # Windows
            self.bind("<Alt-Key-F4>", self.on_closing)

        self.draw_main_frame()

        self.open_app_time = time.time()

    @staticmethod
    def about_dialog():
        tkinter.messagebox.showinfo(title="Accordeur de guitare")

    def draw_settings_frame(self):
        self.main_frame.place_forget()
        self.settings_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def draw_main_frame(self):
        self.settings_frame.place_forget()
        self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def on_closing(self):
        self.audio_analyzer.running = False
        self.play_sound_thread.running = False
        self.destroy()

    def update_color(self):
        self.main_frame.update_color()
        self.settings_frame.update_color()

    def start(self):

        while self.audio_analyzer.running:

            try:

                # prend la fr??quence actuelle dans la queue
                freq = self.frequency_queue.get()
                if freq is not None:

                    # converti la frequence vers le num??ro de la note
                    number = self.audio_analyzer.freq_to_num(freq, self.a4_frequency)

                    # calcule la note la plus proche, la nom de la note et la fr??quence
                    nearest_note_number = round(number)
                    nearest_note_freq = self.audio_analyzer.num_to_freq(nearest_note_number, self.a4_frequency)

                    # calcule la diff??rence de fr??quence entre la note et la note la plus proche
                    freq_difference = nearest_note_freq - freq

                    # calcule la diff??rence de fr??quence (-1)
                    semitone_step = nearest_note_freq - self.audio_analyzer.num_to_freq(round(number - 1),
                                                                                        self.a4_frequency)

                    # calcule l'angle a afficher
                    needle_angle = -90 * ((freq_difference / semitone_step) * 2)

                    # la note actuelle la plus proche change dans le buffer
                    if nearest_note_number != self.nearest_note_number_buffered:
                        self.note_number_counter += 1
                        if self.note_number_counter >= 15:
                            self.nearest_note_number_buffered = nearest_note_number
                            self.note_number_counter = 0

                    # change la couleur du curseur en fonction de sa position
                    if abs(freq_difference) < 1:
                        self.main_frame.set_needle_color("green")
                        self.tone_hit_counter += 1
                    else:
                        self.main_frame.set_needle_color("red")
                        self.tone_hit_counter = 0

                    # met ?? jour le buffer
                    self.needle_buffer_array[:-1] = self.needle_buffer_array[1:]
                    self.needle_buffer_array[-1:] = needle_angle

                    # met ?? jour la gui
                    self.main_frame.set_needle_angle(np.average(self.needle_buffer_array))
                    self.main_frame.set_note_names(
                        note_name=self.audio_analyzer.num_to_note(self.nearest_note_number_buffered),
                        note_name_lower=self.audio_analyzer.num_to_note(self.nearest_note_number_buffered - 1),
                        note_name_higher=self.audio_analyzer.num_to_note(self.nearest_note_number_buffered + 1))

                    # set la fr??quence actuelle
                    if freq is not None: self.main_frame.set_freq(freq)

                self.update()
                self.timer.wait()

            except IOError as err:
                sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(err).__name__, err))
                self.update()
                self.timer.wait()


if __name__ == "__main__":
    app = App()
    app.start()

import tkinter
import tkinter.messagebox
import os
import sys
import json
import requests
import webbrowser
import time
import numpy as np
import random
from distutils.version import StrictVersion as Version

from audio.analyse_audio import AnalyseAudio
from audio.threading_help import ProtectedList
from audio.sound_thread import ThreadAudio

from apparence.color import ColorManager
from apparence.image import ImageManager
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

from settings import Settings


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        if not Settings.COMPILED_APP_MODE:
            if sys.platform == "darwin":  # macOS
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults write -g NSRequiresAquaSystemAppearance -bool No")  # Only for dark-mode testing!
                    # WARNING: This command applies macOS dark-mode on all programs. This can cause bugs on some programs.
                    # Currently this works only with anaconda python version (python.org Tcl/Tk version is only 8.6.8).
                    pass

        tkinter.Tk.__init__(self, *args, **kwargs)

        self.main_path = os.path.dirname(os.path.abspath(__file__))

        self.color_manager = ColorManager()
        self.font_manager = FontManager()
        self.image_manager = ImageManager(self.main_path)
        self.frequency_queue = ProtectedList()

        self.main_frame = Frame(self)
        self.settings_frame = SettingsFrame(self)

        self.audio_analyzer = AnalyseAudio(self.frequency_queue)
        self.audio_analyzer.start()

        self.play_sound_thread = ThreadAudio(self.main_path + "/assets/sounds/drop.wav")
        self.play_sound_thread.start()

        self.timer = Timer(Settings.FPS)

        self.needle_buffer_array = np.zeros(Settings.NEEDLE_BUFFER_LENGTH)
        self.tone_hit_counter = 0
        self.note_number_counter = 0
        self.nearest_note_number_buffered = 69
        self.a4_frequency = 440

        self.dark_mode_active = False

        self.title(Settings.APP_NAME)
        self.geometry(str(Settings.WIDTH) + "x" + str(Settings.HEIGHT))
        self.resizable(True, True)
        self.minsize(Settings.WIDTH, Settings.HEIGHT)
        self.maxsize(Settings.MAX_WIDTH, Settings.MAX_HEIGHT)
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

            app_menu.add_command(label='About ' + Settings.APP_NAME, command=self.about_dialog)
            app_menu.add_separator()

            self.config(menu=menu_bar)

        elif "win" in sys.platform:  # Windows
            self.bind("<Alt-Key-F4>", self.on_closing)

        self.draw_main_frame()



        self.open_app_time = time.time()

    @staticmethod
    def about_dialog():
        tkinter.messagebox.showinfo(title=Settings.APP_NAME,
                                    message=Settings.ABOUT_TEXT)

    def draw_settings_frame(self, event=0):
        self.main_frame.place_forget()
        self.settings_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def draw_main_frame(self, event=0):
        self.settings_frame.place_forget()
        self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)




    def on_closing(self, event=0):
        self.write_user_setting("bell_muted", self.main_frame.button_mute.is_pressed())
        self.check_for_updates()

        if not Settings.COMPILED_APP_MODE:
            if sys.platform == "darwin":  # macOS
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults delete -g NSRequiresAquaSystemAppearance")  # Only for dark-mode testing!
                    # This command reverts the dark-mode setting for all programs.
                    pass

        self.audio_analyzer.running = False
        self.play_sound_thread.running = False
        self.destroy()

    def update_color(self):
        self.main_frame.update_color()
        self.settings_frame.update_color()

    def handle_appearance_mode_change(self):
        dark_mode_state = self.color_manager.detect_os_dark_mode()

        if dark_mode_state is not self.dark_mode_active:
            if dark_mode_state is True:
                self.color_manager.set_mode("Dark")
            else:
                self.color_manager.set_mode("Light")

            self.dark_mode_active = dark_mode_state
            self.update_color()

    def start(self):
        self.handle_appearance_mode_change()



        while self.audio_analyzer.running:

            try:
                # handle the change from dark to light mode, light to dark mode
                self.handle_appearance_mode_change()

                # get the current frequency from the queue
                freq = self.frequency_queue.get()
                if freq is not None:

                    # convert frequency to note number
                    number = self.audio_analyzer.freq_to_num(freq, self.a4_frequency)

                    # calculate nearest note number, name and frequency
                    nearest_note_number = round(number)
                    nearest_note_freq = self.audio_analyzer.num_to_freq(nearest_note_number, self.a4_frequency)

                    # calculate frequency difference from freq to nearest note
                    freq_difference = nearest_note_freq - freq

                    # calculate the frequency difference to the next note (-1)
                    semitone_step = nearest_note_freq - self.audio_analyzer.num_to_freq(round(number-1),
                                                                                                self.a4_frequency)

                    # calculate the angle of the display needle
                    needle_angle = -90 * ((freq_difference / semitone_step) * 2)

                    # buffer the current nearest note number change
                    if nearest_note_number != self.nearest_note_number_buffered:
                        self.note_number_counter += 1
                        if self.note_number_counter >= Settings.HITS_TILL_NOTE_NUMBER_UPDATE:
                            self.nearest_note_number_buffered = nearest_note_number
                            self.note_number_counter = 0

                    # if needle in range +-5 degrees then make it green, otherwise red
                    if abs(freq_difference) < 0.25:
                        self.main_frame.set_needle_color("green")
                        self.tone_hit_counter += 1
                    else:
                        self.main_frame.set_needle_color("red")
                        self.tone_hit_counter = 0

                    # after 7 hits of the right note in a row play the sound
                    if self.tone_hit_counter > 7:
                        self.tone_hit_counter = 0

                        if self.main_frame.button_mute.is_pressed() is not True:
                            self.play_sound_thread.play_sound()

                    # update needle buffer array
                    self.needle_buffer_array[:-1] = self.needle_buffer_array[1:]
                    self.needle_buffer_array[-1:] = needle_angle

                    # update ui note labels and display needle
                    self.main_frame.set_needle_angle(np.average(self.needle_buffer_array))
                    self.main_frame.set_note_names(note_name=self.audio_analyzer.num_to_note(self.nearest_note_number_buffered),
                                                   note_name_lower=self.audio_analyzer.num_to_note(self.nearest_note_number_buffered - 1),
                                                   note_name_higher=self.audio_analyzer.num_to_note(self.nearest_note_number_buffered + 1))

                    # calculate difference in cents
                    if semitone_step == 0:
                        diff_cents = 0
                    else:
                        diff_cents = (freq_difference / semitone_step) * 100
                    freq_label_text = f"+{round(-diff_cents, 1)} cents" if -diff_cents > 0 else f"{round(-diff_cents, 1)} cents"
                    self.main_frame.set_freq_diff(freq_label_text)

                    # set current frequency
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
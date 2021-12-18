import tkinter
from math import sin, radians

from gui.tkinter_button import TkinterCustomButton


class Frame(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master
        self.color_manager = self.app_pointer.color_manager
        self.font_manager = self.app_pointer.font_manager
        self.configure(bg=self.color_manager.background_layer_1)

        self.under_canvas = tkinter.Canvas(master=self,
                                           bg=self.color_manager.background_layer_1,
                                           highlightthickness=0,
                                           height=300,
                                           width=300)

        self.under_canvas.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)

        self.display_outer_circle = self.under_canvas.create_oval(0,
                                                                  0,
                                                                  300 - 1,
                                                                  300 - 1,
                                                                  fill=self.color_manager.theme_main,
                                                                  width=0)

        self.display_background_line = self.under_canvas.create_line(300 * 0.5,
                                                                     300 * 0.5,
                                                                     300 * 0.5,
                                                                     -300 * 0.5,
                                                                     fill=self.color_manager.background_layer_1,
                                                                     width=300 * 0.05)
        self.needle_width = 8
        self.display_needle = self.under_canvas.create_line(300 * 0.5,
                                                            300 * 0.5,
                                                            300 * 0.5,
                                                            300 * 0.05,
                                                            fill=self.color_manager.needle,
                                                            width=self.needle_width,
                                                            capstyle=tkinter.ROUND)

        self.display_inner_circle = self.under_canvas.create_oval(300 * 0.2,
                                                                  300 * 0.2,
                                                                  300 * 0.8,
                                                                  300 * 0.8,
                                                                  fill=self.color_manager.theme_dark,
                                                                  width=0)
        self.bottom_frame = tkinter.Frame(master=self, bg=self.color_manager.background_layer_0)
        self.bottom_frame.place(relx=0, rely=0.5, relheight=0.5, relwidth=1)
        self.upper_canvas = tkinter.Canvas(master=self.bottom_frame,
                                           bg=self.color_manager.background_layer_0,
                                           highlightthickness=0,
                                           height=300 / 2,
                                           width=300)
        self.upper_canvas.place(anchor=tkinter.N, relx=0.5, rely=0)

        self.display_inner_circle_2 = self.upper_canvas.create_oval(300 * 0.2,
                                                                    -300 * 0.3,
                                                                    300 * 0.8,
                                                                    300 * 0.3,
                                                                    fill=self.color_manager.theme_dark,
                                                                    width=0)

        self.note_label = tkinter.Label(master=self,
                                        text="A",
                                        bg=self.color_manager.theme_dark,
                                        fg=self.color_manager.text_2,
                                        font=self.font_manager.note_display_font)
        self.note_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.higher_note_text = self.upper_canvas.create_text(300 * 0.95, 300 * 0.1,
                                                              anchor=tkinter.E,
                                                              text="do",
                                                              fill=self.color_manager.text_2,
                                                              font=self.font_manager.note_display_font_medium)

        self.lower_note_text = self.upper_canvas.create_text(300 * 0.05, 300 * 0.1,
                                                             anchor=tkinter.W,
                                                             text="la",
                                                             fill=self.color_manager.text_2,
                                                             font=self.font_manager.note_display_font_medium)

        self.frequency_text = self.upper_canvas.create_text(300 * 0.5, 300 * 0.16,
                                                            anchor=tkinter.N,
                                                            text="- Hz",
                                                            fill=self.color_manager.text_2,
                                                            font=self.font_manager.frequency_text_font)

        self.button_frequency = TkinterCustomButton(master=self.bottom_frame,
                                                    bg_color=self.color_manager.background_layer_0,
                                                    fg_color=self.color_manager.theme_main,
                                                    hover_color=self.color_manager.theme_light,
                                                    text_font=self.font_manager.button_font,
                                                    text="440 Hz",
                                                    text_color=self.color_manager.text_main,
                                                    corner_radius=10,
                                                    width=150,
                                                    height=40,
                                                    hover=False,
                                                    command=None)
        self.button_frequency.place(anchor=tkinter.SW, relx=0.05, rely=0.9)

    def update_color(self):
        self.configure(bg=self.color_manager.background_layer_1)

        self.under_canvas.configure(bg=self.color_manager.background_layer_1)
        self.under_canvas.itemconfig(self.display_background_line, fill=self.color_manager.background_layer_1)
        self.under_canvas.itemconfig(self.display_outer_circle, fill=self.color_manager.theme_main)
        self.under_canvas.itemconfig(self.display_inner_circle, fill=self.color_manager.theme_dark)

        self.upper_canvas.configure(bg=self.color_manager.background_layer_0)
        self.upper_canvas.itemconfig(self.display_inner_circle_2, fill=self.color_manager.theme_dark)

        self.note_label.configure(bg=self.color_manager.theme_dark, fg=self.color_manager.text_2)

        self.upper_canvas.itemconfig(self.higher_note_text, fill=self.color_manager.text_2)
        self.upper_canvas.itemconfig(self.lower_note_text, fill=self.color_manager.text_2)
        self.upper_canvas.itemconfig(self.frequency_text, fill=self.color_manager.text_2)


        self.bottom_frame.configure(bg=self.color_manager.background_layer_0)

        self.button_frequency.configure_color(bg_color=self.color_manager.background_layer_0,
                                              fg_color=self.color_manager.theme_main,
                                              hover_color=self.color_manager.theme_light,
                                              text_color=self.color_manager.text_main)



    def set_needle_color(self, color):
        if color == "green":
            self.under_canvas.itemconfig(self.display_needle, fill=self.color_manager.needle_hit)
            self.note_label.configure(fg=self.color_manager.text_2_highlight, font=self.font_manager.note_display_font)
        elif color == "red":
            self.under_canvas.itemconfig(self.display_needle, fill=self.color_manager.needle)
            self.note_label.configure(fg=self.color_manager.text_2, font=self.font_manager.note_display_font)

    def set_needle_angle(self, deg):
        x = sin(radians(180 - deg))
        y = sin(radians(270 - deg))

        self.under_canvas.coords(self.display_needle,
                                 300 * 0.5,
                                 300 * 0.5,
                                 300 * 0.5 + (300 * 0.45 * x),
                                 300 * 0.5 + (300 * 0.45 * y))
        return x, y

    def set_note_names(self, note_name, note_name_lower, note_name_higher):
        self.note_label.configure(text=note_name, width=3)
        self.upper_canvas.itemconfig(self.higher_note_text, text=note_name_higher)
        self.upper_canvas.itemconfig(self.lower_note_text, text=note_name_lower)

    def set_freq(self, frequency):
        self.upper_canvas.itemconfig(self.frequency_text, text=str(round(frequency, 1)*2) + " Hz")

    def set_freq_diff(self, frequency):
        self.button_frequency.set_text(str(frequency))

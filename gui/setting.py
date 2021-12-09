import tkinter

from gui.tkinter_button import TkinterCustomButton


class SettingsFrame(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master
        self.color_manager = self.app_pointer.color_manager
        self.font_manager = self.app_pointer.font_manager

        self.configure(bg=self.color_manager.background_layer_1)

        self.bottom_frame = tkinter.Frame(master=self,
                                          bg=self.color_manager.background_layer_0)
        self.bottom_frame.place(anchor=tkinter.S, relx=0.5, rely=1, relheight=0.2, relwidth=1)

        self.button_back = TkinterCustomButton(master=self.bottom_frame,
                                               bg_color=self.color_manager.background_layer_0,
                                               fg_color=self.color_manager.theme_main,
                                               hover_color=self.color_manager.theme_light,
                                               text_font=self.font_manager.button_font,
                                               text="Back",
                                               text_color=self.color_manager.text_main,
                                               corner_radius=10,
                                               width=110,
                                               height=40,
                                               command=self.master.draw_main_frame)
        self.button_back.place(anchor=tkinter.SE, relx=0.95, rely=0.75)

        self.label_note_text = tkinter.Label(master=self,
                                             bg=self.color_manager.background_layer_1,
                                             fg=self.color_manager.text_2,
                                             font=self.font_manager.settings_text_font,
                                             text="A4 =")
        self.label_note_text.place(relx=0.2, rely=0.45, relheight=0.1, relwidth=0.2, anchor=tkinter.CENTER)

        self.label_frequency = TkinterCustomButton(master=self,
                                                   bg_color=self.color_manager.background_layer_1,
                                                   fg_color=self.color_manager.theme_main,
                                                   hover_color=self.color_manager.theme_main,
                                                   text_font=self.font_manager.settings_text_font,
                                                   text="440 Hz",
                                                   text_color=self.color_manager.text_main,
                                                   corner_radius=10,
                                                   width=170,
                                                   height=65,
                                                   hover=False)
        self.label_frequency.place(anchor=tkinter.CENTER, relx=0.5, rely=0.45)

    def update_color(self):
        self.configure(bg=self.color_manager.background_layer_1)
        self.bottom_frame.configure(bg=self.color_manager.background_layer_0)

        self.button_back.configure_color(bg_color=self.color_manager.background_layer_0,
                                         fg_color=self.color_manager.theme_main,
                                         hover_color=self.color_manager.theme_light,
                                         text_color=self.color_manager.text_main)

        self.label_note_text.configure(bg=self.color_manager.background_layer_1, fg=self.color_manager.text_2)

        self.label_frequency.configure_color(bg_color=self.color_manager.background_layer_1,
                                             fg_color=self.color_manager.theme_main,
                                             hover_color=self.color_manager.theme_light,
                                             text_color=self.color_manager.text_main)

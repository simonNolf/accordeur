import tkinter
import sys


class TkinterCustomButton(tkinter.Frame):
    """ boutton customise avec bordure arrondi

        Arguments:  master= ou mettre le boutton
                    bg_color= background color, None est standard,
                    fg_color= foreground color, blue est standard,
                    hover_color= foreground color, lightblue est standard,
                    border_color= foreground color, None est standard,
                    border_width= épaisseur des bordures, 0 est standard,
                    command= callback de la function, None est standard,
                    width= largeur du boutton, 110 est standard,
                    height= hauteur du boutton, 35 est standard,
                    corner_radius= rayon des coins, 10 est standard,
                    text_font= (<Name>, <Size>),
                    text_color= couleur du text, white est standard,
                    text= text du boutton,
                    hover= effet de survol, True est standard"""

    def __init__(self,
                 bg_color=None,
                 fg_color="#2874A6",
                 hover_color="#5499C7",
                 border_color=None,
                 border_width=0,
                 command=None,
                 width=120,
                 height=40,
                 corner_radius=10,
                 text_font=None,
                 text_color="white",
                 text="CustomButton",
                 hover=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if bg_color is None:
            self.bg_color = self.master.cget("bg")
        else:
            self.bg_color = bg_color

        self.fg_color = fg_color
        self.hover_color = hover_color
        self.border_color = border_color

        self.width = width
        self.height = height

        if corner_radius * 2 > self.height:
            self.corner_radius = self.height / 2
        elif corner_radius * 2 > self.width:
            self.corner_radius = self.width / 2
        else:
            self.corner_radius = corner_radius

        self.border_width = border_width

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.text = text
        self.text_color = text_color
        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenger", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 11)
            else:
                self.text_font = "TkDefaultFont"
        else:
            self.text_font = text_font

        self.function = command
        self.hover = hover

        self.configure(width=self.width, height=self.height)

        if sys.platform == "darwin" and self.hover is True:
            self.configure(cursor="pointing-hand")

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     background=self.bg_color,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on)
            self.canvas.bind("<Leave>", self.on)

        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<Button-1>", self.clicked)

        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.text_label = None
        self.image_label = None


    def draw(self):
        self.canvas.delete("all")
        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.canvas.configure(bg=self.bg_color)

        # border button parts
        if self.border_width > 0:

            if self.corner_radius > 0:
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        0,
                                                                        self.corner_radius * 2,
                                                                        self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        0,
                                                                        self.width,
                                                                        self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.corner_radius * 2,
                                                                        self.height))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.width,
                                                                        self.height))

            self.canvas_border_parts.append(self.canvas.create_rectangle(0,
                                                                         self.corner_radius,
                                                                         self.width,
                                                                         self.height - self.corner_radius))
            self.canvas_border_parts.append(self.canvas.create_rectangle(self.corner_radius,
                                                                         0,
                                                                         self.width - self.corner_radius,
                                                                         self.height))

        # inner button parts

        if self.corner_radius > 0:
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.border_width,
                                                                self.border_width + self.inner_corner_radius * 2,
                                                                self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(
                self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                        self.border_width,
                                        self.width - self.border_width,
                                        self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                                self.border_width + self.inner_corner_radius * 2,
                                                                self.height - self.border_width))
            self.canvas_fg_parts.append(
                self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                        self.height - self.border_width - self.inner_corner_radius * 2,
                                        self.width - self.border_width,
                                        self.height - self.border_width))

        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width + self.inner_corner_radius,
                                                                 self.border_width,
                                                                 self.width - self.border_width - self.inner_corner_radius,
                                                                 self.height - self.border_width))
        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width,
                                                                 self.border_width + self.inner_corner_radius,
                                                                 self.width - self.border_width,
                                                                 self.height - self.inner_corner_radius - self.border_width))

        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        for part in self.canvas_border_parts:
            self.canvas.itemconfig(part, fill=self.border_color, width=0)

    def configure_color(self, bg_color=None, fg_color=None, hover_color=None, text_color=None):
        if bg_color is not None:
            self.bg_color = bg_color
        else:
            self.bg_color = self.master.cget("bg")

        if fg_color is not None:
            self.fg_color = fg_color

            # change background color of image_label
            if self.image is not None:
                self.image_label.configure(bg=self.fg_color)

            if self.text_label is not None:
                self.text_label.configure(bg=self.fg_color)

        if hover_color is not None:
            self.hover_color = hover_color

        if text_color is not None:
            self.text_color = text_color

            if self.text_label is not None:
                self.text_label.configure(fg=self.text_color)

        self.draw()

    def set_text(self, text):
        if self.text_label is not None:
            self.text_label.configure(text=text, width=len(text))

    def on(self):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.hover_color, width=0)

        if self.text_label is not None:
            # change background color of image_label
            self.text_label.configure(bg=self.hover_color)

        if self.image_label is not None:
            # change background color of image_label
            self.image_label.configure(bg=self.hover_color)

    def clicked(self):
        if self.function is not None:
            self.function()
            self.on_leave()

import sys


class FontManager(object):
    """ differente police afin que le tout s afficher de la
        meilleur facon possible selon le systeme d'exploitation"""

    def __init__(self):
        # mac os
        if sys.platform == "darwin":
            self.button_font = ("Avenger", 16)
            self.note_display_font = ("Avenger", 72)
            self.note_display_font_medium = ("Avenger", 26)
            self.frequency_text_font = ("Avenger", 15)
            self.info_text_font = ("Avenger", 14)
            self.settings_text_font = ("Avenger", 24)
        # autres systeme d'exploitation
        else:
            self.button_font = ("Century Gothic", 14)
            self.note_display_font = ("Century Gothic", 62)
            self.note_display_font_medium = ("Century Gothic", 24)  # text on left and right site
            self.frequency_text_font = ("Century Gothic", 13)
            self.info_text_font = ("Century Gothic", 12)
            self.settings_text_font = ("Century Gothic", 20)

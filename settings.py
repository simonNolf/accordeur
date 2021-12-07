
class Settings:
    """ GuitarTuner global app configuration """

    COMPILED_APP_MODE = False

    """ general settings """
    APP_NAME = "Accordeur de guitare"
    VERSION = "0.1"
    AUTHOR = "Nolf Simon, Saskia Libotte, Logan, Carlier, Sébastian Hacquin"
    YEAR = "2021"


    WIDTH = 450  # window size when starting the app
    HEIGHT = 440

    MAX_WIDTH = 600  # max window size
    MAX_HEIGHT = 500

    FPS = 60  # canvas update rate
    CANVAS_SIZE = 300  # size of the audio-display

    NEEDLE_BUFFER_LENGTH = 30
    HITS_TILL_NOTE_NUMBER_UPDATE = 15

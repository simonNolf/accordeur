from threading import Lock


class ProtectedList(object):
    """ queue pour partager les données entre les thread avec une protection
        longueur standard du buffer : 8"""

    def __init__(self, buffer_size=8):
        self.elements = []
        self.buffer_size = buffer_size
        self.lock = Lock()

    def put(self, element):
        self.lock.acquire()

        # ajoute un nouvel élément à la fin de la liste
        self.elements.append(element)

        # supprime le puls vieux élément de la liste
        if len(self.elements) > self.buffer_size:
            self.elements.pop(0)

        self.lock.release()

    def get(self):
        self.lock.acquire()

        # vérifie que la liste n est pas vide
        if len(self.elements) > 0:
            element = self.elements[0]
            del self.elements[0]
        else:
            element = None

        self.lock.release()
        return element

    def __repr__(self):
        self.lock.acquire()

        string = str(self.elements)

        self.lock.release()
        return string

from typing import Any


class GamesDTO:
    def __init__(self, success: bool, message: str = "", data: Any = None):
        self.success = success
        self.message = message
        self.data = data

    def Respuesta_Juego(self, juego: object):
        if juego:
            self.success = True
            self.message = "Videjuego encontrado"
            self.data = juego
        else:
            self.success = False
            self.message = "Lo siento, no hemos encontrado el juego que quiere"
            self.data = None
        return self
from typing import Optional
from django_cheems_api.Database.GameData import GameRepository


class Videojuego:
    def __init__(self, id: Optional[int] = None, nombre: str = "", anio: int = 0):
        self.id = id
        self.nombre = nombre
        self.anio = anio

    @classmethod
    def registrar_videojuego(cls, videojuego: "Videojuego"):
        return GameRepository.guardar_videojuego(videojuego)

    @classmethod
    def obtener_videojuegos(cls, busqueda: Optional[str] = None, anio: Optional[int] = None):
        return GameRepository.obtener_videojuegos(busqueda, anio)

    @classmethod
    def obtener_videojuego_por_id(cls, id_videojuego: int):
        return GameRepository.obtener_videojuego_por_id(id_videojuego)

    @classmethod
    def obtener_todos(cls):
        return GameRepository.obtener_todos()

    @classmethod
    def actualizar_videojuego(
        cls,
        id_videojuego: int,
        nombre: Optional[str] = None,
        anio: Optional[int] = None
    ):
        return GameRepository.actualizar_videojuego(id_videojuego, nombre, anio)

    @classmethod
    def eliminar_videojuego(cls, id_videojuego: int):
        return GameRepository.eliminar_videojuego(id_videojuego)

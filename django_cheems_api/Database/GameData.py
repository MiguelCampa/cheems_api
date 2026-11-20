import os
import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GameRepository:
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "Videojuegos"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "charset": "utf8mb4",
        "use_pure": True
    }

    @classmethod
    def _get_connection(cls):
        return mysql.connector.connect(**cls.db_config)

    # CREATE
    @classmethod
    def guardar_videojuego(cls, videojuego: object) -> int:
        conn = cls._get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO videojuegos (nombre, anio) VALUES (%s, %s)",
                (videojuego.nombre.strip(), videojuego.anio)
            )
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Error al guardar videojuego: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # READ
    @classmethod
    def obtener_videojuegos(
        cls,
        busqueda: Optional[str] = None,
        anio: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        conn = cls._get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id_videojuego, nombre, anio FROM videojuegos WHERE 1=1"
            params: List[Any] = []

            if busqueda:
                query += " AND nombre LIKE %s"
                params.append(f"%{busqueda}%")

            if anio is not None:
                query += " AND anio = %s"
                params.append(anio)

            query += " ORDER BY id_videojuego ASC"

            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def obtener_videojuego_por_id(cls, id_videojuego: int) -> Optional[Dict[str, Any]]:
        conn = cls._get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_videojuego, nombre, anio FROM videojuegos WHERE id_videojuego = %s",
                (id_videojuego,)
            )
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def obtener_todos(cls) -> List[Dict[str, Any]]:
        conn = cls._get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id_videojuego, nombre, anio FROM videojuegos ORDER BY id_videojuego ASC")
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # UPDATE
    @classmethod
    def actualizar_videojuego(
        cls,
        id_videojuego: int,
        nombre: Optional[str] = None,
        anio: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        if not cls.obtener_videojuego_por_id(id_videojuego):
            return None

        conn = cls._get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            campos = []
            valores: List[Any] = []

            if nombre is not None:
                campos.append("nombre = %s")
                valores.append(nombre.strip())
            if anio is not None:
                campos.append("anio = %s")
                valores.append(anio)

            if campos:
                valores.append(id_videojuego)
                cursor.execute(
                    f"UPDATE videojuegos SET {', '.join(campos)} WHERE id_videojuego = %s",
                    tuple(valores)
                )
                conn.commit()

            return cls.obtener_videojuego_por_id(id_videojuego)
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Error al actualizar videojuego: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # DELETE
    @classmethod
    def eliminar_videojuego(cls, id_videojuego: int) -> bool:
        conn = cls._get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM videojuegos WHERE id_videojuego = %s", (id_videojuego,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Error al eliminar videojuego: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

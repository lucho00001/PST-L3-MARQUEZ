from . import store
from .schemas import LecturaEntrada, ComandoLED

def guardar_lectura(datos: LecturaEntrada) -> dict:
    lectura = datos.model_dump()
    store.lecturas.append(lectura)
    # Conservamos como máximo las últimas 100 lecturas recibidas.
    del store.lecturas[:-100]
    return {"lectura": lectura, "led": store.estado_led["color"]}

def listar_lecturas() -> list[dict]:
    return store.lecturas

def consultar_led() -> dict:
    return store.estado_led

def cambiar_led(comando: ComandoLED) -> dict:
    store.estado_led["color"] = comando.color
    return store.estado_led


def calcular_promedio(n: int) -> dict | None:
    ultimas = store.lecturas[-n:]

    if not ultimas:
        return None

    cantidad = len(ultimas)

    return {
        "cantidad": cantidad,
        "temperatura_promedio": round(
            sum(dato["temperatura"] for dato in ultimas) / cantidad, 2
        ),
        "humedad_promedio": round(
            sum(dato["humedad"] for dato in ultimas) / cantidad, 2
        )
    }

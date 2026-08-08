NODOS_SISTEMA = [
    "Núcleo IA",
    "Input Usuario", 
    "Procesador NLP", 
    "Memoria Vectorial", 
    "Generador de Respuestas", 
    "API Externa"
]

ENLACES_SISTEMA = [
    ("Núcleo IA", "Input Usuario"),
    ("Núcleo IA", "Procesador NLP"),
    ("Núcleo IA", "Memoria Vectorial"),
    ("Núcleo IA", "Generador de Respuestas"),
    ("Núcleo IA", "API Externa")
]

CONFIGURACION_MODULOS = {
    "Núcleo IA": {
        "descripcion": "El cerebro central del sistema. Orquesta la comunicación entre todos los módulos.",
        "config": {"Estado": "Latiendo", "Carga CPU": "12%", "Conexiones": "5"}
    },
    "Input Usuario": {
        "descripcion": "Módulo encargado de la captura de texto y voz en tiempo real.",
        "config": {"Estado": "Escuchando", "Idioma": "Español"}
    },
    "Procesador NLP": {
        "descripcion": "Motor de comprensión de lenguaje y análisis de intención.",
        "config": {"Estado": "Activo", "Modelo": "Local-Llama3"}
    },
    "Memoria Vectorial": {
        "descripcion": "Base de datos semántica para recordar el contexto a largo plazo.",
        "config": {"Estado": "Conectado", "Vectores": "1.2M"}
    },
    "Generador de Respuestas": {
        "descripcion": "Módulo final que estructura y renderiza la salida hacia el usuario.",
        "config": {"Estado": "En espera", "Temperatura": "0.7"}
    },
    "API Externa": {
        "descripcion": "Conexión a herramientas web y búsqueda de información en vivo.",
        "config": {"Estado": "Inactivo", "Peticiones": "0"}
    }
}

def obtener_datos_modulo(nombre_modulo):
    datos = CONFIGURACION_MODULOS.get(nombre_modulo)
    if datos:
        return datos["descripcion"], datos["config"]
    else:
        return "Módulo no registrado.", {"Estado": "Desconocido"}
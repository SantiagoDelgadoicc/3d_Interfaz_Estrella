from ursina import *
import networkx as nx
import math
from panel_ui import PanelConfiguracion
import datos_ia

app = Ursina(title="Cerebro IA 3D")
window.color = color.hex("#000000")

nodo_arrastrado = None
pos_inicial_drag = None

lista_aristas = []
diccionario_nodos = {}

velocidad_regreso = 1.5

vel_actual_y = 10.0
vel_objetivo_y = 10.0

vel_actual_x = 2.0
vel_objetivo_x = 2.0

fov_objetivo = 40.0

cam_offset_seleccion = Vec3(4, 0, -10)
cam_rotacion_seleccion = Vec3(0, 0, 0)

nodo_seleccionado = None

control_camara = False
modo_camara = 'normal'

cam_destino = Vec3(0, 0, -30)
cam_mirada = Vec3(0, 0, 0)

centro_grafo = Entity()

editor_camera = None


def posicion_centro_ia():
    if "Núcleo IA" in diccionario_nodos:
        return diccionario_nodos["Núcleo IA"].world_position

    return Vec3(0, 0, 0)


def direccion_a_rotacion(direccion):

    direccion = direccion.normalized()

    yaw = math.degrees(
        math.atan2(
            direccion.x,
            direccion.z
        )
    )

    pitch = math.degrees(
        math.asin(
            max(-1, min(1, direccion.y))
        )
    )

    return Vec3(
        -pitch,
        yaw,
        0
    )


def calcular_camara_nodo(nodo):

    posicion = Vec3(nodo.world_position)

    referencia = Entity(
        position=posicion,
        rotation=Vec3(camera.rotation)
    )

    derecha = Vec3(referencia.right)
    adelante = Vec3(referencia.forward)

    destroy(referencia)

    distancia = 11.0
    desplazamiento_lateral = 2.0

    destino_camara = (
        posicion
        - adelante * distancia
        + derecha * desplazamiento_lateral
    )

    punto_mirada = (
        posicion
        + derecha * 2.0
    )

    return (
        destino_camara,
        punto_mirada
    )

def calcular_camara_centro():

    posicion = posicion_centro_ia()

    return (
        posicion + Vec3(0, 0, -30),
        direccion_a_rotacion(
            posicion - (
                posicion + Vec3(0, 0, -30)
            )
        )
    )


def reanudar_rotacion():

    global vel_objetivo_y
    global vel_objetivo_x
    global fov_objetivo
    global nodo_seleccionado
    global control_camara
    global modo_camara
    global cam_destino
    global cam_mirada

    vel_objetivo_y = 10.0
    vel_objetivo_x = 2.0

    fov_objetivo = 40.0

    if nodo_seleccionado:
        nodo_seleccionado.color = (
            nodo_seleccionado.color_original
        )

    nodo_seleccionado = None

    modo_camara = 'regresando'

    cam_destino, cam_mirada = (
        calcular_camara_centro()
    )

    control_camara = True


mi_panel = PanelConfiguracion(
    callback_al_cerrar=reanudar_rotacion
)


def procesar_clic_nodo(nodo_entidad):

    global vel_objetivo_y
    global vel_objetivo_x
    global vel_actual_y
    global vel_actual_x
    global fov_objetivo
    global nodo_seleccionado
    global control_camara
    global modo_camara
    global cam_destino
    global cam_mirada

    if nodo_seleccionado:
        nodo_seleccionado.color = (
            nodo_seleccionado.color_original
        )

    nodo_seleccionado = nodo_entidad

    nodo_seleccionado.color = color.hex("#d1b448")

    vel_objetivo_y = 0.0
    vel_objetivo_x = 0.0

    vel_actual_y = 0.0
    vel_actual_x = 0.0

    fov_objetivo = 25.0

    cam_destino, cam_mirada = calcular_camara_nodo(
        nodo_entidad
    )

    modo_camara = 'acercando'

    control_camara = True

    nombre_modulo = nodo_entidad.name

    descripcion, configuracion = (
        datos_ia.obtener_datos_modulo(
            nombre_modulo
        )
    )

    posicion_tarjeta = Vec2(
        0.2,
        0.05
    )

    mi_panel.abrir_con_datos(
        nombre_modulo,
        descripcion,
        configuracion,
        posicion_tarjeta
    )

def input(key):

    global nodo_arrastrado
    global pos_inicial_drag

    if key == 'right mouse down' or key == 'right mouse up':
        mouse.locked = False
        return

    if key == 'left mouse down':

        if (
            mouse.hovered_entity
            and hasattr(
                mouse.hovered_entity,
                'es_nodo'
            )
        ):

            nodo_arrastrado = (
                mouse.hovered_entity
            )

            pos_inicial_drag = (
                mouse.position
            )

    elif key == 'left mouse up':

        if nodo_arrastrado:

            distancia = (
                (mouse.x - pos_inicial_drag.x) ** 2
                +
                (mouse.y - pos_inicial_drag.y) ** 2
            )

            if distancia < 0.001:

                procesar_clic_nodo(
                    nodo_arrastrado
                )

            nodo_arrastrado = None


def construir_grafo(
    datos_nodos,
    datos_enlaces
):

    global lista_aristas
    global diccionario_nodos

    for hijo in centro_grafo.children:
        destroy(hijo)

    lista_aristas.clear()
    diccionario_nodos.clear()

    G = nx.Graph()

    G.add_edges_from(
        datos_enlaces
    )

    posiciones = nx.spring_layout(
        G,
        dim=3,
        iterations=100
    )

    escala = 6

    for nodo_id, p in posiciones.items():

        es_centro = (
            nodo_id == "Núcleo IA"
        )

        color_nodo = (
            color.hex("#a88427")
            if es_centro
            else color.hex("#d1ac3b")
        )

        tamano = (
            1.2
            if es_centro
            else 0.5
        )

        nodo = Entity(
            parent=centro_grafo,
            model='sphere',
            color=color_nodo,
            scale=tamano,
            position=(
                float(p[0] * escala),
                float(p[1] * escala),
                float(p[2] * escala)
            ),
            collider='sphere',
            name=nodo_id
        )

        nodo.posicion_original = (
            Vec3(nodo.position)
        )

        nodo.es_nodo = True
        nodo.es_centro = es_centro

        nodo.color_original = (
            color_nodo
        )

        diccionario_nodos[
            nodo_id
        ] = nodo

        texto_nodo = Text(
            parent=centro_grafo,
            text=nodo_id,
            billboard=True,
            origin=(0, 0),
            position=(
                nodo.position
                +
                Vec3(
                    0,
                    -1.5
                    if not es_centro
                    else -1.9,
                    0
                )
            ),
            scale=7,
            color=color.white
        )

        nodo.texto_nombre = (
            texto_nodo
        )

    for arista in datos_enlaces:

        n1 = diccionario_nodos[
            arista[0]
        ]

        n2 = diccionario_nodos[
            arista[1]
        ]

        linea_ent = Entity(
            parent=centro_grafo,
            model=Mesh(
                vertices=[
                    n1.position,
                    n2.position
                ],
                mode='line',
                thickness=1.5
            ),
            color=color.hex("#6b541c"),
        )

        lista_aristas.append({
            'entidad': linea_ent,
            'n1': n1,
            'n2': n2
        })


def actualizar_camara():

    global control_camara
    global modo_camara

    if not control_camara:
        return

    rotacion_destino = direccion_a_rotacion(
        cam_mirada - camera.position
    )

    camera.position = lerp(
        camera.position,
        cam_destino,
        time.dt * 0.9
    )

    camera.rotation = lerp(
        camera.rotation,
        rotacion_destino,
        time.dt * 0.9
    )

    camera.fov = lerp(
        camera.fov,
        fov_objetivo,
        time.dt * 0.9
    )

    distancia = distance(
        camera.position,
        cam_destino
    )

    diferencia_rotacion = distance(
        camera.rotation,
        rotacion_destino
    )

    diferencia_fov = abs(
        camera.fov -
        fov_objetivo
    )

    if (
        distancia < 0.05
        and diferencia_rotacion < 0.5
        and diferencia_fov < 0.5
    ):

        camera.position = Vec3(
            cam_destino
        )

        camera.rotation = direccion_a_rotacion(
            cam_mirada -
            camera.position
        )

        camera.fov = fov_objetivo

        if modo_camara == 'regresando':

            control_camara = False
            modo_camara = 'normal'

            if editor_camera:
                editor_camera.enabled = True

def update():

    
    global vel_actual_y
    global vel_actual_x

    if mouse.right:
        mouse.right = False

    if nodo_arrastrado:

        nodo_arrastrado.world_position += (
            camera.right
            *
            mouse.velocity[0]
            *
            50
        )

        nodo_arrastrado.world_position += (
            camera.up
            *
            mouse.velocity[1]
            *
            50
        )

    else:

        for n in diccionario_nodos.values():

            distancia = distance(
                n.position,
                n.posicion_original
            )

            if distancia > 0.01:

                n.position = lerp(
                    n.position,
                    n.posicion_original,
                    time.dt *
                    velocidad_regreso
                )

    for arista in lista_aristas:

        arista[
            'entidad'
        ].model.vertices = [
            arista['n1'].position,
            arista['n2'].position
        ]

        arista[
            'entidad'
        ].model.generate()

    vel_actual_y = lerp(
        vel_actual_y,
        vel_objetivo_y,
        time.dt * 4
    )

    vel_actual_x = lerp(
        vel_actual_x,
        vel_objetivo_x,
        time.dt * 4
    )

    centro_grafo.rotation_y += (
        vel_actual_y *
        time.dt
    )

    centro_grafo.rotation_x += (
        vel_actual_x *
        time.dt
    )

    actualizar_camara()

    for n in diccionario_nodos.values():

        if getattr(
            n,
            'es_centro',
            False
        ):

            n.scale = (
                1.2
                +
                math.sin(
                    time.time() * 3
                ) * 0.1
            )

        if hasattr(
            n,
            'texto_nombre'
        ):

            n.texto_nombre.position = (
                n.position
                +
                Vec3(
                    0,
                    -1.5
                    if not n.es_centro
                    else -1.9,
                    0
                )
            )

            distancia = distance(
                camera.world_position,
                n.world_position
            )

            escala_texto = (
                distancia * 0.22
            )

            escala_texto = max(
                4.0,
                min(
                    9.0,
                    escala_texto
                )
            )

            if n.es_centro:
                escala_texto *= 0.85

            n.texto_nombre.scale = (
                escala_texto
            )


if __name__ == '__main__':

    construir_grafo(
        datos_ia.NODOS_SISTEMA,
        datos_ia.ENLACES_SISTEMA
    )

    editor_camera = EditorCamera(
        rotation_speed=0,
        pan_speed=0
    )

    editor_camera.right_mouse = False

    app.run()
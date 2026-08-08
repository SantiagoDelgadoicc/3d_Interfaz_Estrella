from ursina import *

class PanelConfiguracion:
    def __init__(self, callback_al_cerrar):
        self.panel = Entity(parent=camera.ui, enabled=False)
        
        self.fondo = Entity(parent=self.panel, model='quad', color= (0.1, 0.1, 0.1, 0.8)  , scale=(0.5, 0.6), z=0.1)
        
        self.callback_al_cerrar = callback_al_cerrar

        self.titulo = Text(parent=self.panel, text="", position=(-0.23, 0.25), scale=1.3, color=color.cyan)
        self.descripcion = Text(parent=self.panel, text="", position=(-0.23, 0.15), scale=0.85) 
        
        self.lbl_config = Text(parent=self.panel, text="Tablero de Configuración:", position=(-0.23, -0.05), scale=1, color=color.yellow)
        self.tablero_config = Text(parent=self.panel, text="", position=(-0.23, -0.12), scale=0.85)

        self.btn_cerrar = Button(parent=self.panel, text='X', scale=(0.04, 0.04), position=(0.21, 0.26), color=color.red)
        self.btn_cerrar.on_click = self.cerrar

    def abrir_con_datos(self, nombre, desc, config_dict, posicion_pantalla):
        """Inyecta los datos y ubica el panel al lado del nodo"""
        
        self.panel.position = posicion_pantalla
        
        self.titulo.text = nombre
        self.descripcion.text = desc
        self.descripcion.wordwrap = 40 
        
        texto_config = "\n".join([f"• {k}: {v}" for k, v in config_dict.items()])
        self.tablero_config.text = texto_config
        
        self.panel.enabled = True

    def cerrar(self):
        self.panel.enabled = False
        if self.callback_al_cerrar:
            self.callback_al_cerrar()
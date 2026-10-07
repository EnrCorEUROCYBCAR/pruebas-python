import sys
import json # Importamos la librería para manejar JSON
import os   # Para comprobar si el archivo existe

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QVBoxLayout, QHBoxLayout, QLineEdit, 
                               QPushButton, QListWidget, QMessageBox)

class GestorTareas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Gestor de Tareas con Guardado")
        self.resize(400, 450)

        # Archivo donde guardaremos los datos
        self.archivo_datos = "mis_tareas.json"

        # --- INTERFAZ GRÁFICA (Igual que antes) ---
        widget_central = QWidget()
        layout_principal = QVBoxLayout()

        layout_superior = QHBoxLayout()
        self.input_tarea = QLineEdit()
        self.input_tarea.setPlaceholderText("¿Qué necesitas hacer hoy?")
        self.btn_anadir = QPushButton("Añadir")
        layout_superior.addWidget(self.input_tarea)
        layout_superior.addWidget(self.btn_anadir)

        self.lista_tareas = QListWidget()

        layout_inferior = QHBoxLayout()
        self.btn_eliminar = QPushButton("Eliminar Seleccionada")
        self.btn_limpiar = QPushButton("Borrar Todo")
        layout_inferior.addWidget(self.btn_eliminar)
        layout_inferior.addWidget(self.btn_limpiar)

        layout_principal.addLayout(layout_superior)
        layout_principal.addWidget(self.lista_tareas)
        layout_principal.addLayout(layout_inferior)

        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        # --- CONEXIONES ---
        self.btn_anadir.clicked.connect(self.anadir_tarea)
        self.input_tarea.returnPressed.connect(self.anadir_tarea)
        self.btn_eliminar.clicked.connect(self.eliminar_tarea)
        self.btn_limpiar.clicked.connect(self.limpiar_tareas)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f2f5; }
            QPushButton { background-color: #0078D7; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #005a9e; }
            QListWidget { border: 1px solid #ccc; border-radius: 4px; font-size: 14px; padding: 5px; }
            QLineEdit { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        """)

        # --- CARGAR LOS DATOS AL INICIAR ---
        self.cargar_tareas()

    # --- NUEVAS FUNCIONES DE GUARDADO Y CARGA ---

    def cargar_tareas(self):
        """Lee el archivo JSON al abrir el programa y rellena la lista."""
        if os.path.exists(self.archivo_datos): # Comprueba si el archivo ya existe
            with open(self.archivo_datos, 'r', encoding='utf-8') as archivo:
                # Convertimos el texto del JSON a una lista de Python
                tareas_guardadas = json.load(archivo)
                # Añadimos cada tarea a nuestro QListWidget
                for tarea in tareas_guardadas:
                    self.lista_tareas.addItem(tarea)

    def guardar_tareas(self):
        """Recorre la lista, extrae los textos y los guarda en el JSON."""
        tareas_para_guardar = []
        # Recorremos todas las filas de la lista
        for i in range(self.lista_tareas.count()):
            item = self.lista_tareas.item(i)
            tareas_para_guardar.append(item.text())
        
        # Escribimos la lista en el archivo JSON
        with open(self.archivo_datos, 'w', encoding='utf-8') as archivo:
            # ensure_ascii=False permite que se guarden bien las tildes y las eñes
            json.dump(tareas_para_guardar, archivo, ensure_ascii=False, indent=4)

    # --- EVENTO DE CIERRE DE VENTANA ---
    
    def closeEvent(self, evento):
        """Este método es especial de PySide. Se ejecuta automáticamente al darle a la 'X'."""
        self.guardar_tareas() # Guardamos todo
        evento.accept()       # Dejamos que la ventana se cierre con normalidad

    # --- LÓGICA ANTERIOR (Añadir, eliminar, limpiar) ---

    def anadir_tarea(self):
        texto = self.input_tarea.text().strip()
        if texto:
            self.lista_tareas.addItem(texto)
            self.input_tarea.clear()
        else:
            QMessageBox.warning(self, "Error", "¡No puedes añadir una tarea vacía!")

    def eliminar_tarea(self):
        fila_actual = self.lista_tareas.currentRow()
        if fila_actual >= 0:
            self.lista_tareas.takeItem(fila_actual)
        else:
            QMessageBox.information(self, "Aviso", "Selecciona una tarea para eliminar.")

    def limpiar_tareas(self):
        if self.lista_tareas.count() > 0:
            respuesta = QMessageBox.question(self, "Confirmar", "¿Seguro que quieres borrar todas las tareas?", 
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if respuesta == QMessageBox.StandardButton.Yes:
                self.lista_tareas.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestorTareas()
    ventana.show()
    sys.exit(app.exec())
import sqlite3
import sys
from pathlib import Path
import datetime

def establecer_conexion(nombre_archivo_bd: str) -> sqlite3.Connection:
    """Establece conexion activando el parseo de fechas enseñado en clase."""
    try:
        conexion_activa = sqlite3.connect(
            nombre_archivo_bd,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        return conexion_activa
    except sqlite3.Error:
        print("Error critico: No se pudo establecer conexion con la base de datos.")
        sys.exit()

def verificar_estado_almacenamiento(nombre_archivo_bd: str) -> sqlite3.Connection:
    """Usa pathlib para LBYL y verifica la existencia fisica del archivo y tablas."""
    ruta_bd = Path(nombre_archivo_bd)
    archivo_existe = ruta_bd.is_file()
    
    conexion_activa = establecer_conexion(nombre_archivo_bd)
    cursor_verificacion = conexion_activa.cursor()
    
    cursor_verificacion.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name IN ('Clientes', 'Platillos', 'Turnos', 'Pedidos', 'Detalles_Pedido')
    """)
    tablas_encontradas = cursor_verificacion.fetchall()
    cantidad_tablas = len(tablas_encontradas)
    
    if not archivo_existe or cantidad_tablas == 0:
        print("Aviso: No se encontro almacenamiento previo. Iniciando base de datos vacia.")
        construir_estructura_tablas(conexion_activa)
        insertar_turnos_por_defecto(conexion_activa)
    elif cantidad_tablas < 5:
        print("Error critico de almacenamiento: Faltan archivos de sujetos del programa.")
        sys.exit()
        
    return conexion_activa

def construir_estructura_tablas(conexion_activa: sqlite3.Connection) -> None:
    """Genera las tablas aplicando el tipo timestamp para las fechas."""
    cursor_creacion = conexion_activa.cursor()
    
    cursor_creacion.execute("""
        CREATE TABLE IF NOT EXISTS Clientes (
            IdCliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL
        )
    """)
    
    cursor_creacion.execute("""
        CREATE TABLE IF NOT EXISTS Turnos (
            Id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_turno TEXT NOT NULL UNIQUE
        )
    """)
    
    cursor_creacion.execute("""
        CREATE TABLE IF NOT EXISTS Platillos (
            IdPlatillo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_Platillo TEXT NOT NULL UNIQUE
        )
    """)
    
    cursor_creacion.execute("""
        CREATE TABLE IF NOT EXISTS Pedidos (
            Id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_Cliente INTEGER NOT NULL,
            Id_turno INTEGER NOT NULL,
            fecha_evento timestamp NOT NULL,
            nombre_evento TEXT NOT NULL,
            estado TEXT DEFAULT 'Activo',
            fecha_registro timestamp NOT NULL,
            FOREIGN KEY (Id_Cliente) REFERENCES Clientes (IdCliente),
            FOREIGN KEY (Id_turno) REFERENCES Turnos (Id_turno)
        )
    """)
    
    cursor_creacion.execute("""
        CREATE TABLE IF NOT EXISTS Detalles_Pedido (
            Id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_pedido INTEGER NOT NULL,
            Id_Platillo INTEGER NOT NULL,
            Porciones INTEGER NOT NULL CHECK(Porciones > 0),
            FOREIGN KEY (Id_pedido) REFERENCES Pedidos (Id_pedido),
            FOREIGN KEY (Id_Platillo) REFERENCES Platillos (IdPlatillo)
        )
    """)
    
    conexion_activa.commit()

def insertar_turnos_por_defecto(conexion_activa: sqlite3.Connection) -> None:
    """Usa placeholders (?) para insertar datos iniciales."""
    cursor_insercion = conexion_activa.cursor()
    turnos_iniciales = [("Matutino",), ("Vespertino",), ("Nocturno",)]
    
    cursor_insercion.executemany("""
        INSERT OR IGNORE INTO Turnos (nombre_turno) VALUES (?)
    """, turnos_iniciales)
    
    conexion_activa.commit()

def inicializar_sistema() -> sqlite3.Connection:
    nombre_base_datos = "sistema_catering.db"
    conexion_principal = verificar_estado_almacenamiento(nombre_base_datos)
    return conexion_principal

def registrar_cliente(conexion_activa: sqlite3.Connection, nombre: str, apellidos: str) -> None:
    """Inserta un nuevo registro en la tabla Clientes y muestra el ID generado automaticamente."""
    try:
        cursor_insercion = conexion_activa.cursor()
        
        cursor_insercion.execute("""
            INSERT INTO Clientes (nombre, apellidos) 
            VALUES (?, ?)
        """, (nombre, apellidos))
        
        conexion_activa.commit()
        id_generado = cursor_insercion.lastrowid
        
        print(f"\n[Exito] Cliente registrado correctamente. Clave asignada: {id_generado}")
        
    except sqlite3.Error:
        print("\n[!] Error critico: No se pudo registrar el cliente en la base de datos.")
if __name__ == "__main__":
    conexion_app = inicializar_sistema()
    print("El sistema backend esta listo y protegido.")


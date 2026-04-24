import sys
import backend
import validaciones

def mostrar_menu_principal() -> str:
    """Despliega las opciones principales y captura la eleccion del usuario."""
    print("\n" + "="*50)
    print("   SISTEMA DE GESTION DE CATERING CORPORATIVO")
    print("="*50)
    print("1. Registrar un nuevo cliente")
    print("2. Registrar un nuevo platillo")
    print("3. Registrar un pedido")
    print("4. Obtener reportes")
    print("5. Editar evento de un pedido")
    print("6. Cancelar un pedido")
    print("7. Salir del sistema")
    print("="*50)
    
    opcion_seleccionada = input("Por favor, elija una opcion (1-7): ").strip()
    return opcion_seleccionada

def ejecutar_aplicacion() -> None:
    """Ciclo principal de la aplicacion que controla el flujo del menu."""
    
    # Arranca la base de datos antes de mostrar el menu
    conexion_base_datos = backend.inicializar_sistema()
    
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == '1':
            print("\n--- Modulo: Registrar Nuevo Cliente ---")
            nombre_cliente = validaciones.pedir_texto_obligatorio("Ingrese el nombre del cliente: ")
            apellidos_cliente = validaciones.pedir_texto_obligatorio("Ingrese los apellidos del cliente: ")
            
            backend.registrar_cliente(conexion_base_datos, nombre_cliente, apellidos_cliente)
            
        elif opcion == '2':
            print("\n--- Modulo: Registrar Platillo ---")
            print("En construccion...")
            
        elif opcion == '3':
            print("\n--- Modulo: Registrar Pedido ---")
            print("En construccion...")
            
        elif opcion == '4':
            print("\n--- Modulo: Reportes ---")
            print("En construccion...")
            
        elif opcion == '5':
            print("\n--- Modulo: Editar Pedido ---")
            print("En construccion...")
            
        elif opcion == '6':
            print("\n--- Modulo: Cancelar Pedido ---")
            print("En construccion...")
            
        elif opcion == '7':
            print("\nCerrando el sistema y guardando estado...")
            conexion_base_datos.close()
            sys.exit()
            
        else:
            print("\n[!] Error: Opcion invalida. Por favor seleccione un numero del 1 al 7.")

if __name__ == "__main__":
    ejecutar_aplicacion()
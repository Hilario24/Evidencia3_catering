def pedir_texto_obligatorio(mensaje_solicitud: str) -> str:
    """Solicita texto al usuario repetidamente hasta que ingrese una cadena valida (no vacia ni solo espacios)."""
    while True:
        entrada_usuario = input(mensaje_solicitud).strip()
        
        if entrada_usuario:
            return entrada_usuario
            
        print("[!] Error de validacion: El texto no puede estar vacio o contener unicamente espacios.")
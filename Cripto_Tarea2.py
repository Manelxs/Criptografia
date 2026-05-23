import string
import random

class SistemaCifradoAlberti:
    def __init__(self):
        # Configuración del disco de Alberti (Fijo e Interno desordenado)
        self.disco_externo = string.ascii_uppercase
        self.disco_interno = "qzxrtyuipasdfghjklwcvbnmoe"
        
        # Usamos una lista de diccionarios para asegurar que el orden de arriba 
        # hacia abajo se mantenga perfectamente según el momento de creación.
        self.historial_mensajes = []
        
        # Clave interna fija para el movimiento polialfabético del disco
        self.clave_alberti = "ALBERTI"

    def _obtener_indice_desplazamiento(self, letra_clave):
        letra_mayus = letra_clave.upper()
        if letra_mayus in self.disco_externo:
            return self.disco_externo.index(letra_mayus)
        return 0

    def _cifrar(self, mensaje):
        mensaje_cifrado = []
        num_clave = len(self.clave_alberti)
        
        for i, letra in enumerate(mensaje):
            if not letra.isalpha():
                mensaje_cifrado.append(letra)
                continue
                
            letra_clave_actual = self.clave_alberti[i % num_clave]
            desplazamiento = self._obtener_indice_desplazamiento(letra_clave_actual)
            idx_externo = self.disco_externo.index(letra.upper())
            idx_interno = (idx_externo + desplazamiento) % len(self.disco_interno)
            mensaje_cifrado.append(self.disco_interno[idx_interno])
            
        return "".join(mensaje_cifrado)

    def _descifrar(self, mensaje_cifrado):
        mensaje_claro = []
        num_clave = len(self.clave_alberti)
        
        for i, letra in enumerate(mensaje_cifrado):
            if not letra.isalpha():
                mensaje_claro.append(letra)
                continue
                
            letra_clave_actual = self.clave_alberti[i % num_clave]
            desplazamiento = self._obtener_indice_desplazamiento(letra_clave_actual)
            idx_interno = self.disco_interno.index(letra.lower())
            idx_externo = (idx_interno - desplazamiento) % len(self.disco_externo)
            mensaje_claro.append(self.disco_externo[idx_externo])
            
        return "".join(mensaje_claro)

    def registrar_y_encriptar(self, mensaje_original):
        """Cifra el mensaje, genera una llave única de 6 dígitos y lo guarda en el historial."""
        if not mensaje_original.strip():
            return None, "El mensaje no puede estar vacío."
            
        # Obtener todas las llaves existentes para evitar duplicados
        llaves_existentes = [registro["llave"] for registro in self.historial_mensajes]
        
        while True:
            llave_unica = str(random.randint(100000, 999999))
            if llave_unica not in llaves_existentes:
                break
                
        texto_cifrado = self._cifrar(mensaje_original)
        
        # Guardamos un diccionario con los datos del registro al final del historial
        nuevo_registro = {
            "llave": llave_unica,
            "texto_cifrado": texto_cifrado
        }
        self.historial_mensajes.append(nuevo_registro)
        
        return llave_unica, texto_cifrado

    def recuperar_y_desencriptar(self, llave_unica):
        """Busca la llave en el historial y descifra el mensaje si existe."""
        for registro in self.historial_mensajes:
            if registro["llave"] == llave_unica:
                return self._descifrar(registro["texto_cifrado"])
        return None

    def obtener_historial(self):
        """Devuelve la lista ordenada con todos los registros."""
        return self.historial_mensajes


# ==========================================
# Interfaz de Usuario por Consola (Menú)
# ==========================================
def menu():
    sistema = SistemaCifradoAlberti()
    
    while True:
        print("\n" + "="*45)
        print("    SISTEMA DE CIFRADO DE ALBERTI")
        print("="*45)
        print("1. Encriptar una palabra / mensaje")
        print("2. Desencriptar usando Llave Única")
        print("3. Ver lista de palabras encriptadas")
        print("4. Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            print("\n--- ENCRIPTAR MENSAJE ---")
            palabra = input("Introduce la palabra o frase a encriptar: ")
            llave, cifrado = sistema.registrar_y_encriptar(palabra)
            
            if llave:
                print("\n[✓] ¡Mensaje Encriptado con éxito!")
                print(f"-> Texto Cifrado: {cifrado}")
                print(f"-> TU LLAVE ÚNICA DE RECUPERACIÓN: {llave}")
                print("Guarda bien esta llave, la necesitarás para recuperar el mensaje.")
            else:
                print(f"[X] Error: {cifrado}")
                
        elif opcion == "2":
            print("\n--- DESENCRIPTAR MENSAJE ---")
            llave_ingresada = input("Introduce la Llave Única de 6 dígitos: ").strip()
            
            resultado = sistema.recuperar_y_desencriptar(llave_ingresada)
            
            if resultado is not None:
                print("\n[✓] ¡Mensaje Recuperado!")
                print(f"-> Palabra/Frase original: {resultado}")
            else:
                print("\n[X] Error: La llave introducida no existe o es incorrecta.")
                
        elif opcion == "3":
            print("\n--- LISTA DE PALABRAS ENCRIPTADAS ---")
            historial = sistema.obtener_historial()
            
            if not historial:
                print("[!] No hay ninguna palabra encriptada en el sistema todavía.")
            else:
                # Estructura visual de la tabla limpia y formateada
                print(f"{'N°':<4} | {'LLAVE ÚNICA':<12} | {'TEXTO ENCRIPTADO'}")
                print("-" * 50)
                
                # Recorremos de arriba hacia abajo con un índice ascendente (empezando en 1)3
                for indice, registro in enumerate(historial, start=1):
                    llave = registro["llave"]
                    texto_enc = registro["texto_cifrado"]
                    print(f"{indice:<4} | {llave:<12} | {texto_enc}")
                    
                print("-" * 50)
                print(f"Total de registros: {len(historial)}")
                
        elif opcion == "4":
            print("\n¡Gracias por usar el simulador de Alberti! Saliendo del programa...")
            break
        else:
            print("\n[X] Opción no válida. Por favor, introduce un número del 1 al 4.")

if __name__ == "__main__":
    menu()
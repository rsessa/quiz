import os
import re

# --- Configuración ---
html_input_filename = "index.html"      # Archivo HTML principal
js_data_filename = "datos_quiz.js"     # Archivo JS con los datos
html_output_filename = "movil.html"    # Archivo HTML de salida autocontenido

# --- Lógica ---

def create_standalone_html():
    """Lee los archivos HTML y JS, y crea una versión HTML autocontenida."""
    try:
        # 1. Leer el contenido del archivo JS de datos
        print(f"Leyendo datos desde '{js_data_filename}'...")
        with open(js_data_filename, 'r', encoding='utf-8') as f_js:
            js_data_content = f_js.read()

        # Escapar las barras invertidas para evitar errores con secuencias Unicode
        js_data_content = js_data_content.replace("\\", "\\\\")
        print("Datos JS leídos correctamente.")

        # 2. Leer el contenido del archivo HTML principal
        print(f"Leyendo estructura desde '{html_input_filename}'...")
        with open(html_input_filename, 'r', encoding='utf-8') as f_html:
            html_content = f_html.read()
        print("HTML leído correctamente.")

        # 3. Preparar el bloque de script para incrustar
        #    Se añade una capa extra de <script> tags alrededor del contenido leído
        embedded_script_block = f"<script>\n// Contenido de {js_data_filename} incrustado:\n{js_data_content}\n</script>"

        # 4. Buscar y reemplazar la etiqueta <script src="datos_quiz.js">
        #    Usamos regex para ser un poco más flexibles con espacios o comillas
        script_src_pattern = re.compile(r'<script\s+src=["\']' + re.escape(js_data_filename) + r'["\']\s*></script>', re.IGNORECASE)

        # Reemplazar la etiqueta encontrada con el bloque de script incrustado
        new_html_content, num_replacements = script_src_pattern.subn(embedded_script_block, html_content)

        if num_replacements == 0:
            print(f"Advertencia: No se encontró la etiqueta '<script src=\"{js_data_filename}\"></script>' en '{html_input_filename}'.")
            print("Se añadirá el script de datos al final del <head>, pero revisa tu HTML.")
            # Como fallback, intentar insertar antes de </head> (menos ideal)
            head_end_pattern = re.compile(r'</head>', re.IGNORECASE)
            new_html_content, num_head_replacements = head_end_pattern.subn(f"{embedded_script_block}\n</head>", html_content)
            if num_head_replacements == 0:
                 print(f"Error: No se pudo encontrar ni la etiqueta <script src> ni </head> en '{html_input_filename}'. No se puede generar '{html_output_filename}'.")
                 return # Salir si no se puede insertar

        elif num_replacements > 1:
             print(f"Advertencia: Se encontraron {num_replacements} etiquetas '<script src=\"{js_data_filename}\"></script>'. Todas fueron reemplazadas por el contenido incrustado.")


        # 5. Escribir el nuevo contenido en el archivo de salida
        print(f"Escribiendo archivo autocontenido en '{html_output_filename}'...")
        with open(html_output_filename, 'w', encoding='utf-8') as f_out:
            f_out.write(new_html_content)
        print(f"¡Archivo '{html_output_filename}' generado exitosamente!")

    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo '{e.filename}'.")
        print("Asegúrate de que tanto '{html_input_filename}' como '{js_data_filename}' existen en la misma carpeta que este script.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --- Ejecución Principal ---
if __name__ == "__main__":
    create_standalone_html()

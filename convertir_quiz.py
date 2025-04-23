import re
import json # Usaremos json para escapar correctamente las cadenas para JS

# --- Configuración ---
input_filename = "notebooklm_output.txt"  # Nombre del archivo de entrada (salida de NotebookLM)
output_filename = "datos_quiz.js"        # Nombre del archivo de salida JavaScript
default_quiz_title = "Cuestionario: Administración de Sistemas Operativos (Generado)" # Título por defecto

# --- Funciones ---

def escape_js_string(value):
    """Escapa una cadena para usarla de forma segura dentro de comillas dobles en JavaScript."""
    # json.dumps añade comillas dobles y escapa caracteres necesarios (como \n, \", \\)
    return json.dumps(value)

def parse_notebooklm_output(text):
    """Analiza el texto de entrada y extrae las preguntas."""
    questions = []
    # Regex para encontrar bloques de preguntas
    # re.DOTALL hace que '.' coincida también con saltos de línea
    question_blocks = re.findall(r'\[\[QUESTION_START\]\](.*?)\[\[QUESTION_END\]\]', text, re.DOTALL)

    print(f"Se encontraron {len(question_blocks)} bloques de preguntas.")

    question_counter = 1 # Para asignar un número secuencial 'n'

    for block in question_blocks:
        question_data = {
            "n": question_counter, # Número secuencial asignado por el script
            "pregunta": "",
            "opciones": {},
            "correcta": "",
            "justificacion": ""
        }
        # Banderas para saber si encontramos los campos obligatorios
        found_question = False
        found_options = {'a': False, 'b': False, 'c': False, 'd': False}
        found_correct = False
        found_justification = False

        lines = block.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line: # Ignorar líneas vacías
                continue

            # Usar regex para extraer datos de forma más flexible
            match_q = re.match(r'Question:\s*(.*)', line, re.IGNORECASE)
            match_a = re.match(r'OptionA:\s*(.*)', line, re.IGNORECASE)
            match_b = re.match(r'OptionB:\s*(.*)', line, re.IGNORECASE)
            match_c = re.match(r'OptionC:\s*(.*)', line, re.IGNORECASE)
            match_d = re.match(r'OptionD:\s*(.*)', line, re.IGNORECASE)
            match_correct = re.match(r'Correct:\s*([a-d])', line, re.IGNORECASE) # Solo capturar a, b, c, o d
            match_just = re.match(r'Justification:\s*(.*)', line, re.IGNORECASE)
            # Ignorar la línea Number: si existe
            match_num = re.match(r'Number:\s*\d+', line, re.IGNORECASE)

            if match_q:
                question_data["pregunta"] = match_q.group(1).strip()
                found_question = True
            elif match_a:
                question_data["opciones"]["a"] = match_a.group(1).strip()
                found_options['a'] = True
            elif match_b:
                question_data["opciones"]["b"] = match_b.group(1).strip()
                found_options['b'] = True
            elif match_c:
                question_data["opciones"]["c"] = match_c.group(1).strip()
                found_options['c'] = True
            elif match_d:
                question_data["opciones"]["d"] = match_d.group(1).strip()
                found_options['d'] = True
            elif match_correct:
                question_data["correcta"] = match_correct.group(1).lower() # Guardar en minúscula
                found_correct = True
            elif match_just:
                question_data["justificacion"] = match_just.group(1).strip()
                found_justification = True
            elif match_num:
                pass # Ignorar la línea del número original
            else:
                 print(f"Advertencia: Línea no reconocida en el bloque {question_counter}: '{line[:50]}...'")


        # Validar si se encontraron todos los campos necesarios
        missing_fields = []
        if not found_question: missing_fields.append("Question")
        if not all(found_options.values()): missing_fields.append("todas las Options (A,B,C,D)")
        if not found_correct: missing_fields.append("Correct")
        if not found_justification: missing_fields.append("Justification")

        if not missing_fields:
            questions.append(question_data)
            question_counter += 1
        else:
            print(f"Error: Pregunta omitida (bloque aprox. {question_counter}) por faltar campos: {', '.join(missing_fields)}")
            print(f"--- Bloque problemático --- \n{block.strip()}\n------------------------")


    return questions

def format_as_js(title, questions):
    """Formatea los datos como un string para el archivo datos_quiz.js."""
    js_output = []
    # Añadir el título
    js_output.append(f"const quizTitle = {escape_js_string(title)};")
    js_output.append("\n") # Doble salto de línea
    js_output.append("const quizData = [")

    # Añadir cada pregunta formateada
    for i, q in enumerate(questions):
        js_output.append("  {")
        js_output.append(f"    n: {q['n']}, // Originalmente bloque {i+1}") # Usar el 'n' asignado
        js_output.append(f"    pregunta: {escape_js_string(q['pregunta'])},")
        js_output.append("    opciones: {")
        # Asegurar que las opciones a,b,c,d siempre estén presentes
        js_output.append(f"      a: {escape_js_string(q['opciones'].get('a', 'Opción A no encontrada'))},")
        js_output.append(f"      b: {escape_js_string(q['opciones'].get('b', 'Opción B no encontrada'))},")
        js_output.append(f"      c: {escape_js_string(q['opciones'].get('c', 'Opción C no encontrada'))},")
        js_output.append(f"      d: {escape_js_string(q['opciones'].get('d', 'Opción D no encontrada'))}")
        js_output.append("    },")
        js_output.append(f"    correcta: {escape_js_string(q['correcta'])},")
        js_output.append(f"    justificacion: {escape_js_string(q['justificacion'])}")
        js_output.append("  }" + ("," if i < len(questions) - 1 else "")) # Coma al final, excepto en el último

    js_output.append("];")
    return "\n".join(js_output)

# --- Ejecución Principal ---
if __name__ == "__main__":
    try:
        # Leer el archivo de entrada completo
        with open(input_filename, 'r', encoding='utf-8') as f:
            input_text = f.read()
        print(f"Archivo '{input_filename}' leído correctamente.")

        # Parsear el texto
        parsed_questions = parse_notebooklm_output(input_text)

        if not parsed_questions:
             print("No se pudieron parsear preguntas válidas. No se generará el archivo de salida.")
        else:
            # Formatear como JavaScript
            js_content = format_as_js(default_quiz_title, parsed_questions)
            print(f"Se procesaron {len(parsed_questions)} preguntas válidas.")

            # Escribir el archivo de salida
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(js_content)
            print(f"Archivo '{output_filename}' generado exitosamente.")

    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_filename}' no fue encontrado.")
        print("Asegúrate de que el archivo exista en la misma carpeta que este script y que el nombre sea correcto.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


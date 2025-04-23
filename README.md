# Cuestionario Interactivo

Aplicación web para realizar un cuestionario interactivo sobre cualquier tema que quieras estudiar/repasar, diseñada con HTML, CSS y JavaScript puro.

## Características Principales

* **Interfaz Interactiva:** 
    Preguntas presentadas en tarjetas individuales con animación de volteo 3D al responder.
* **Feedback Visual:** 
    Indicación clara e instantánea de respuesta correcta (verde, ✓) o incorrecta (rojo, X).
* **Justificaciones:** 
    Muestra la justificación para las respuestas correctas, con notas sobre posibles discrepancias entre la fuente original y la información pública.
* **Múltiples Intentos:** 
    Permite reintentar las preguntas falladas, registrando el número de intentos.
* **Orden Aleatorio y Límite:** 
    Las preguntas se barajan cada vez que se carga la página. Si hay más de 20 preguntas disponibles, se seleccionan aleatoriamente 20 para el cuestionario.
* **Responsive y Mobile-First:** 
    Diseño adaptable que funciona correctamente en dispositivos móviles, tablets y escritorios.
* **Barra de Progreso:** 
    Indica visualmente el avance del usuario en el cuestionario.
* **Datos Incrustados (Generados):** 
    Las preguntas y el título se definen en un archivo `datos_quiz.js` que se *genera* a partir de otras fuentes (ver "Flujo de Trabajo").
* **Resumen Final:** 
    Muestra un resumen con el número de aciertos, porcentaje, intentos totales y una clasificación simple.
* **Información Adicional:** 
    Incluye una nota con el número total de preguntas disponibles en la base de datos original y un pie de página con información del autor.

## Flujo de Trabajo y Uso

Esta aplicación está diseñada para funcionar directamente desde el archivo `index.html`. Sin embargo, la gestión de las preguntas se realiza mediante un flujo específico:

1.  **Generación de Preguntas:** 
    Utiliza un modelo de lenguaje (como NotebookLM) con el prompt proporcionado en `prompt_notebooklm.txt` y tus fuentes de información para generar un listado estructurado de preguntas. Guarda esta salida en un archivo llamado `notebooklm_output.txt`en la misma carpeta que el script de Python `convertir_quiz.py`.
2.  **Conversión a JavaScript:** 
    Ejecuta el script de Python `convertir_quiz.py`. Este script leerá `notebooklm_output.txt` y generará automáticamente el archivo `datos_quiz.js` con las preguntas formateadas correctamente.

    ```bash
    python convertir_quiz.py
    ```
3.  **Ejecución:** 
    Abre el archivo `index.html` en tu navegador web. Este archivo cargará los datos desde el `datos_quiz.js` recién generado.

**Nota:** El archivo `datos_quiz.js` no necesita estar versionado en el repositorio, ya que se genera a partir de los otros archivos mediante el script.

## Estructura de Archivos en el Repositorio

* `index.html`: Contiene la estructura HTML, los estilos CSS y la lógica principal de JavaScript de la aplicación. Carga los datos desde `datos_quiz.js`.
* `convertir_quiz.py`: Script de Python para procesar la salida de texto estructurado (generada por NotebookLM) y crear el archivo `datos_quiz.js`.
* `prompt_notebooklm.txt` (Recomendado): Archivo de texto que contiene el prompt utilizado para generar las preguntas con NotebookLM.

## Colaboración IA

Este proyecto fue desarrollado en colaboración con un asistente de IA (Google Gemini 2,5 Pro) a través de un proceso de "ViveCoding", refinando iterativamente el código y las funcionalidades.

## Autor

* **Richard Sessa Alcaraz** - [rsessa](https://github.com/rsessa)


## Licencia

Este proyecto se distribuye bajo una licencia Copyleft 🄯 2024. Eres libre de usar, modificar y distribuir el código, siempre y cuando mantengas esta libertad para otros y reconozcas la autoría original.

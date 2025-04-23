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
* **Datos Separados (Escritorio) / Incrustados (Móvil):**
    * La versión principal (`index.html`) carga las preguntas y el título desde un archivo JavaScript externo (`datos_quiz.js`), facilitando su mantenimiento.
    * Se proporciona un script (`version_movil.py`) para crear una versión autocontenida (`movil.html`) con los datos incrustados, ideal para distribución y uso sin servidor, especialmente en móviles.
* **Resumen Final:**
    Muestra un resumen con el número de aciertos, porcentaje, intentos totales y una clasificación simple.
* **Información Adicional:**
    Incluye una nota con el número total de preguntas disponibles en la base de datos original y un pie de página con información del autor.

## Flujo de Trabajo y Uso

Esta aplicación está diseñada para funcionar directamente desde el archivo `index.html` (o `movil.html`). Sin embargo, la gestión de las preguntas se realiza mediante un flujo específico:

1.  **Generación de Preguntas:**
    Utiliza un modelo de lenguaje (como NotebookLM) con el prompt proporcionado en `prompt_notebooklm.txt` y tus fuentes de información para generar un listado estructurado de preguntas. Guarda esta salida en un archivo llamado `notebooklm_output.txt` en la misma carpeta que el script de Python `convertir_quiz.py`.
2.  **Conversión a JavaScript:**
    Ejecuta el script de Python `convertir_quiz.py`. Este script leerá `notebooklm_output.txt` y generará automáticamente el archivo `datos_quiz.js` con las preguntas formateadas correctamente.
    ```bash
    python convertir_quiz.py
    ```
3.  **Generación Versión Móvil/Standalone (Opcional):**
    Si necesitas una versión que funcione sin servidor local (ideal para móviles o distribución simple), ejecuta el script `version_movil.py`. Este script combinará `index.html` y `datos_quiz.js` en un único archivo `movil.html`.
    ```bash
    python version_movil.py
    ```
4.  **Ejecución:**
    * **Para `movil.html`:** Abre el archivo `movil.html` directamente en cualquier navegador web. Funcionará sin necesidad de servidor.
    * **Para `index.html`:** Debido a las restricciones CORS si te da error al cargar `datos_quiz.js` desde `file://`, necesitas un servidor local simple.
        * Navega a la carpeta del proyecto en tu terminal.
        * Inicia el servidor: `python -m http.server` (Python 3).
        * Abre tu navegador y ve a `http://localhost:8000` (o el puerto indicado) y haz clic en `index.html`.


## Estructura de Archivos en el Repositorio

* `index.html`: Versión principal de la aplicación. Carga datos desde `datos_quiz.js`. **Requiere servidor local para funcionar correctamente.**
* `convertir_quiz.py`: Script de Python para procesar la salida de texto estructurado (generada por NotebookLM) y crear el archivo `datos_quiz.js`.
* `version_movil.py`: Script de Python para generar la versión autocontenida `movil.html` a partir de `index.html` y `datos_quiz.js`.
* `prompt_notebooklm.txt` (Recomendado): Archivo de texto que contiene el prompt utilizado para generar las preguntas con NotebookLM.


## Colaboración IA

Este proyecto fue desarrollado en colaboración con un asistente de IA (Google Gemini 2,5 Pro) a través de un proceso de "ViveCoding", refinando iterativamente el código y las funcionalidades.

## Autor

* **Richard Sessa Alcaraz** - [rsessa](https://github.com/rsessa)

## Licencia

Este proyecto se distribuye bajo una licencia Copyleft 🄯 2024. Eres libre de usar, modificar y distribuir el código, siempre y cuando mantengas esta libertad para otros y reconozcas la autoría original.

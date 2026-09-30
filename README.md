# Sprint 9: Proyecto Urban Routes - TripleTen

Este proyecto contiene una prueba automatizada de extremo a extremo para validar el flujo de solicitud de un taxi Comfort en **Urban Routes**. La prueba configura la ruta, agrega teléfono y tarjeta, escribe un mensaje, selecciona extras y comprueba que aparezca la información del conductor.

## 📂 Estructura del proyecto

- `data.py` → URL y datos de prueba en constantes
- `pages.py` → Page Object, localizadores y acciones de Selenium
- `main.py` → Escenarios y verificaciones con pytest
- `requirements.txt` → Dependencias del proyecto

## 🛠️ Tecnologías utilizadas

- **Python** para el código de automatización
- **Selenium WebDriver** para interactuar con la aplicación web
- **Pytest** para ejecutar la prueba

## ⚙️ Requisitos e instalación

- Python 3.12 o compatible
- Google Chrome

Instala las dependencias desde la carpeta del proyecto:

```powershell
py -m pip install -r requirements.txt
```

## 🧪 Ejecutar las pruebas

```powershell
py -m pytest main.py -v
```

La opción `-v` muestra el resultado detallado.

## 📌 Notas

- Cada prueba abre y cierra su propia sesión de Chrome.
- Puedes ejecutar un escenario aislado, por ejemplo: `py -m pytest main.py -v -k test_add_card`.
- La URL y los datos se pueden cambiar en `data.py`.
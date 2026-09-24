# Sprint 9: Proyecto Urban Routes - TripleTen

Este proyecto contiene una prueba automatizada de extremo a extremo para validar el flujo de solicitud de un taxi Comfort en **Urban Routes**. La prueba configura la ruta, agrega teléfono y tarjeta, escribe un mensaje, selecciona extras y comprueba que aparezca la información del conductor.

---

## 📂 Estructura del proyecto

- `data.py` → URL de Urban Routes y datos utilizados en la prueba
- `main.py` → Localizadores, métodos de página y prueba automatizada con Selenium y pytest

## ⚙️ Requisitos

- Python 3.12 o compatible
- Google Chrome
- Librerías necesarias: `selenium` y `pytest`

Instalación de dependencias:

```powershell
py -m pip install selenium pytest
```

## 🛠️ Tecnologías utilizadas

- **Python** para el código de automatización
- **Selenium WebDriver** para interactuar con la aplicación web
- **Pytest** para ejecutar la prueba

## 🧪 Ejecutar la prueba

Desde la carpeta del proyecto, ejecuta:

```powershell
py -m pytest main.py -v
```

La opción `-v` muestra el resultado detallado. Selenium abrirá Google Chrome; mantén el navegador abierto mientras se ejecuta la prueba.

## 📌 Notas

- La URL y los datos de prueba se pueden modificar en `data.py`.
- La prueba completa está en `test_complete_taxi_order`, dentro de `main.py`.

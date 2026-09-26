# Sprint 9: Proyecto Urban Routes - TripleTen

Pruebas automatizadas de extremo a extremo para validar la solicitud de un taxi Comfort en **Urban Routes**, desde la configuración de la ruta hasta la asignación del conductor.

## 📂 Estructura del proyecto

- `data.py` → URL y datos de prueba en constantes
- `pages.py` → Page Object, localizadores y acciones de Selenium
- `main.py` → Escenarios y verificaciones con pytest
- `requirements.txt` → Dependencias del proyecto

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

Las pruebas avanzan secuencialmente en una misma sesión del navegador. Selenium abrirá Chrome; mantenlo abierto durante la ejecución. La URL y los datos se pueden cambiar en `data.py`.

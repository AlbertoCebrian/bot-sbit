#  Bot de Automatización para sBit

Este script automatiza el proceso de rellenar la ficha diaria de prácticas en la plataforma sBit. Navega automáticamente por el calendario y ficha las horas correspondientes en los días que estén vacíos (0H).

##  Instalación y Configuración

Sigue estos pasos en orden para configurar el bot en tu ordenador. Es necesario tener [Python](https://www.python.org/downloads/) instalado.

### 1. Descargar el proyecto
Descarga este repositorio en tu ordenador (botón verde "Code" > "Download ZIP" y descomprímelo) o clónalo usando Git:
```bash
git clone [https://github.com/AlbertoCebrian/bot-sbit.git](https://github.com/AlbertoCebrian/bot-sbit.git)
```

### 2. Preparar el entorno virtual
Abre una terminal dentro de la carpeta del proyecto y ejecuta los comandos correspondientes a tu sistema operativo:

**En Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
*(Nota: Sabrás que está activado porque verás `(.venv)` al principio de la línea en tu terminal).*

### 3. Instalar dependencias
Con el entorno activado, instala las herramientas necesarias ejecutando:

```bash
# Instalar las librerías de Python
pip install -r requirements.txt

# Descargar el motor del navegador (Chromium)
playwright install chromium
```

### 4. Configurar tus datos
Abre el archivo `bot.py` con cualquier editor de texto o código y rellena tus datos personales en el bloque superior de **CONFIGURACIÓN**:

* `USUARIO`: Tu nombre de usuario de sBit (ej: "20s0crhi").
* `PASSWORD`: Tu contraseña de sBit.
* `MESES_ATRAS`: Cuántos meses hacia atrás debe ir el calendario para empezar a buscar días. Si estamos en Abril y tienes q marcar 2 meses , desde febrero, pones un 2.
* `DIA_INICIO`: El número del día exacto del mes donde quieres empezar (ej: "1" o "10").
* `FECHA_FIN`: La fecha exacta donde el bot se detendrá. **Debe estar escrito IGUAL que en la web** (ej: "3 de desembre de 2025").

---

##  Cómo usar el bot

Una vez configurado todo, asegúrate de tener el entorno virtual activado (`.\.venv\Scripts\activate`) y ejecuta en la terminal:

```bash
python bot.py
```

 **Importante:** Se abrirá una ventana del navegador automáticamente. **No la cierres ni interactúes con la página** mientras el bot esté trabajando. En la terminal podrás ver un registro (log) de lo que está haciendo paso a paso.

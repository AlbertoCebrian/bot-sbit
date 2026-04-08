import time
import re
from playwright.sync_api import sync_playwright

def run():
    # =========================================================================
    # 1. CONFIGURACIÓN DE USUARIO 
    # =========================================================================
    
    USUARIO = "tu_usuario_aqui"    # <--- Cambia esto por tu usuario de sBit
    PASSWORD = "tu_password_aqui"  # <--- Cambia esto por tu contraseña
    
    # ¿Cuántos meses hacia atrás debe ir el calendario para empezar?
    # (Si hoy es Abril y quieres empezar en Febrero, pon 2)
    MESES_ATRAS = 2 
    
    # ¿Qué número de día del mes quieres que clique para empezar?
    DIA_INICIO = "1" 

    # Fecha exacta donde el bot se detendrá. 
    # DEBE estar escrito IGUAL que aparece en la cabecera de la web.
    FECHA_FIN = "3 de desembre de 2025"

    # Horas a fichar (debe ser el valor del desplegable: "4.0", "5.0", "8.0")
    HORAS = "4.0"

    # =========================================================================
    # 2. INICIO DEL PROCESO (EL BOT HACE TODO LO DEMÁS, NO TOCAR)
    # =========================================================================

    with sync_playwright() as p:
        # Abrimos el navegador (slow_mo ayuda a que la web no se bloquee)
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        print(f"--- Iniciando Bot para: {USUARIO} ---")
        page.goto("https://www.empresaiformacio.org/sBid")
        
        # El sBid funciona con IFrames (ventanas dentro de ventanas)
        # Definimos el marco principal
        frame_principal = page.frame_locator('iframe[name="jspContainer"]')

        # Aceptar Cookies si aparecen
        try:
            frame_principal.get_by_role("button", name=re.compile("Acceptar|Aceptar", re.IGNORECASE)).click(timeout=3000)
        except:
            pass 

        # Proceso de Login
        print("Introduciendo credenciales...")
        frame_principal.get_by_role("textbox", name="Usuari").fill(USUARIO)
        frame_principal.get_by_role("textbox", name="Contrasenya").fill(PASSWORD)
        
        # Clic en el botón de entrar (buscamos el botón de tipo submit)
        frame_principal.get_by_role("button").filter(has_text=re.compile(r".*", re.DOTALL)).last.click()
        
        print("Esperando al panel de control...")
        page.wait_for_load_state('networkidle')
        time.sleep(3) 

        # Definimos el marco del contenido donde está el calendario
        frame_cal = frame_principal.frame_locator('iframe[name="contentmain"]')

        # Navegamos hacia atrás en los meses
        print(f"Retrocediendo {MESES_ATRAS} meses...")
        for _ in range(MESES_ATRAS):
            try:
                frame_cal.get_by_role("cell", name="Disminuir mes").click()
                time.sleep(0.8)
            except:
                print("Aviso: No se pudo retroceder más el mes.")
                break

        # Clic en el día de inicio
        print(f"Buscando el día {DIA_INICIO}...")
        try:
            frame_cal.get_by_text(DIA_INICIO, exact=True).first.click()
            time.sleep(2)
        except:
            print("ERROR: No se encontró el día. Revisa la configuración.")
            return

        # Entrar en la ficha diaria
        print("Accediendo a la actividad diaria...")
        try:
            frame_cal.get_by_role("link", name="Activitat diària del dossier").first.click()
        except:
            print("ERROR: No se encontró el enlace de la actividad. ¿Ya está abierto?")
            return

        # BUCLE DE FICHADO AUTOMÁTICO
        while True:
            time.sleep(1.5) 
            
            # 1. Comprobar si hemos terminado
            if frame_cal.get_by_text(FECHA_FIN).is_visible():
                print(f"¡Objetivo alcanzado! Llegamos al {FECHA_FIN}.")
                break

            # 2. Comprobar si el día está vacío (0H introducidas)
            dia_vacio = frame_cal.get_by_text("Hores introduïdes").locator("..").get_by_text("0H")
            
            if dia_vacio.is_visible():
                print("Día vacío detectado. Fichando...")
                dropdown = frame_cal.locator("select[name^='inp_']").first
                if dropdown.is_visible():
                    dropdown.select_option(HORAS)
                    frame_cal.get_by_text("Emmagatzemar").click()
                    page.wait_for_load_state('networkidle')
                    time.sleep(1)
                else:
                    print("No se puede editar (posible festivo o fin de semana).")
            else:
                print("Día ya fichado o no editable. Saltando...")

            # 3. Ir al día siguiente
            boton_siguiente = frame_cal.get_by_role("link", name="Següent")
            if boton_siguiente.is_visible():
                boton_siguiente.click()
            else:
                print("No hay más días disponibles.")
                break

        print("--- Proceso completado con éxito ---")
        # browser.close() 

if __name__ == "__main__":
    run()
# CP-CN-015
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

service = Service(executable_path=r"C:\chromedriver-win64\chromedriver.exe")

options = Options()
options.add_argument(r"--user-data-dir=C:\Users\user\selenium-profile")
options.add_argument("--start-maximized")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://teammates-libelula2.uc.r.appspot.com/web/front/home")

wait = WebDriverWait(driver, 30)

try:
    # Intentar login si el botón está visible
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        login_button.click()

        instructor_login = wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn")))
        instructor_login.click()
        print("Sesión iniciada.")
    except TimeoutException:
        print("Ya estás logueado. Continuando...")

    # --- NAVEGACIÓN AUTOMÁTICA ---
    # Paso 1: Hacer clic en Sessions
    sessions_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@href='/web/instructor/sessions' and contains(@class, 'nav-link')]")
    ))
    sessions_link.click()
    print("Navegando a Sessions...")

    # Paso 2: Hacer clic en el botón Edit
    edit_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'btn') and contains(text(), 'Edit')]")
    ))
    edit_button.click()
    print("Haciendo clic en Edit...")

    # Dar tiempo para que cargue la página de edición
    time.sleep(3)

    # === NUEVA FUNCIONALIDAD: PREVIEW AS STUDENT ===
    print("--- INICIANDO PREVIEW AS STUDENT ---")

    try:
        # Buscar el botón "Preview as Student"
        print("Buscando botón 'Preview as Student'...")

        # Estrategia 1: Buscar por ID
        try:
            preview_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-preview-student")))
            print("✓ Botón encontrado por ID")
        except TimeoutException:
            # Estrategia 2: Buscar por texto
            try:
                preview_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Preview as Student')]")
                ))
                print("✓ Botón encontrado por texto")
            except TimeoutException:
                # Estrategia 3: Buscar por clase y texto combinados
                preview_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Preview')]")
                ))
                print("✓ Botón encontrado por clase y texto")

        # Hacer scroll al botón
        print("Haciendo scroll al botón Preview as Student...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", preview_button)
        time.sleep(2)

        # Intentar hacer clic normal primero
        try:
            preview_button.click()
            print("✓ Clic normal exitoso en Preview as Student")
        except Exception:
            # Si el clic normal falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", preview_button)
            print("✓ Clic con JavaScript exitoso en Preview as Student")

        print("✓ Preview as Student ejecutado exitosamente")

    except Exception as e:
        print(f"❌ Error al hacer clic en Preview as Student: {e}")

        # Tomar captura de pantalla para debug
        try:
            driver.save_screenshot("preview_student_error.png")
            print("Captura guardada como preview_student_error.png")
        except:
            pass

        input("PAUSA: Verifica manualmente y presiona ENTER...")

    print("--- PREVIEW AS STUDENT COMPLETADO ---")

    # Esperar a que el usuario presione ENTER antes de cerrar sesión
    input("Presiona ENTER para cerrar sesión...")

    # --- CERRAR SESIÓN ---
    # Paso 1: abrir el menú desplegable haciendo clic en el botón con tu correo
    profile_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'jcoronado@unsa.edu.pe')]")
    ))
    profile_button.click()

    # Paso 2: hacer clic en el botón Log Out
    logout_button = wait.until(EC.element_to_be_clickable((By.ID, "logout-btn")))
    logout_button.click()
    print("Sesión cerrada.")

except Exception as e:
    print(f"Ocurrió un error: {type(e).__name__}")
    print(f"Mensaje completo: {str(e)}")

    # Intentar tomar una captura de pantalla para debug
    try:
        driver.save_screenshot("error_screenshot.png")
        print("Captura de pantalla guardada como error_screenshot.png")
    except:
        pass

    input("Presiona ENTER para continuar con el debug...")

finally:
    driver.quit()
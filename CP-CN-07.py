#CP-CN-023
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuración del servicio de ChromeDriver
service = Service(executable_path=r"C:\chromedriver-win64\chromedriver.exe")

# Opciones del navegador
options = Options()
options.add_argument(r"--user-data-dir=C:\Users\user\selenium-profile")
options.add_argument("--start-maximized")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--remote-debugging-port=9222")

# Iniciar navegador
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://teammates-libelula2.uc.r.appspot.com/web/front/home")

wait = WebDriverWait(driver, 30)

try:
    # Intentar login si es necesario
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        login_button.click()

        instructor_login = wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn")))
        instructor_login.click()
        print("Sesión iniciada.")
    except TimeoutException:
        print("Ya estás logueado. Continuando...")

    # Esperar botón "Add New Course" (aunque no lo usemos ahora)
    print("Esperando botón 'Add New Course'...")
    add_course_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Add New Course')]")))
    add_course_btn.click()

    # Hacer clic en "Other Actions" del primer curso
    print("Buscando botón 'Other Actions'...")
    other_actions_btn = wait.until(EC.element_to_be_clickable((By.ID, "btn-other-actions-0")))
    driver.execute_script("arguments[0].scrollIntoView(true);", other_actions_btn)
    time.sleep(1)  # Espera breve para que termine de desplazarse
    driver.execute_script("arguments[0].click();", other_actions_btn)
    print("Se hizo clic en 'Other Actions'.")

    # Hacer clic en el botón "Edit" en lugar de "Archive"
    print("Esperando botón 'Edit'...")
    edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit')]")))
    edit_btn.click()
    print("Se hizo clic en 'Edit'.")

    # Esperar a que cargue la nueva página de edición
    print("Esperando que cargue la página de edición...")
    time.sleep(2)

    # === NUEVA FUNCIONALIDAD: ADD NEW INSTRUCTOR ===
    print("--- INICIANDO PROCESO DE AGREGAR INSTRUCTOR ---")

    # Paso 1: Hacer clic en "Add New Instructor"
    print("Buscando botón 'Add New Instructor'...")
    try:
        add_instructor_btn = wait.until(EC.element_to_be_clickable((By.ID, "btn-add-instructor")))

        # Hacer scroll al botón
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_instructor_btn)
        time.sleep(2)

        # Intentar clic normal primero
        try:
            add_instructor_btn.click()
            print("✓ Clic normal exitoso en Add New Instructor")
        except Exception:
            # Si falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", add_instructor_btn)
            print("✓ Clic con JavaScript exitoso en Add New Instructor")

    except Exception as e:
        print(f"❌ Error al hacer clic en Add New Instructor: {e}")
        input("PAUSA: Verifica manualmente y presiona ENTER...")

    # Dar tiempo para que aparezca el formulario
    time.sleep(3)

    # Paso 2: Llenar el campo de nombre
    print("Llenando campo de nombre...")
    try:
        name_field = wait.until(EC.element_to_be_clickable((By.ID, "name-instructor-2")))

        # Hacer scroll al campo
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", name_field)
        time.sleep(1)

        name_field.clear()
        name_field.send_keys("yimi charca")
        print("✓ Nombre 'yimi charca' escrito correctamente")

    except Exception as e:
        print(f"❌ Error al escribir nombre: {e}")

    # Paso 3: Llenar el campo de email
    print("Llenando campo de email...")
    try:
        email_field = wait.until(EC.element_to_be_clickable((By.ID, "email-instructor-2")))

        # Hacer scroll al campo
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", email_field)
        time.sleep(1)

        email_field.clear()
        email_field.send_keys("ycharca@unsa.edu.pe")
        print("✓ Email 'ycharca@unsa.edu.pe' escrito correctamente")

    except Exception as e:
        print(f"❌ Error al escribir email: {e}")

    # Paso 4: Seleccionar rol Manager
    print("Seleccionando rol Manager...")
    try:
        manager_radio = wait.until(EC.element_to_be_clickable((By.ID, "INSTRUCTOR_PERMISSION_ROLE_MANAGER11")))

        # Hacer scroll al radio button
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", manager_radio)
        time.sleep(1)

        # Intentar clic normal primero
        try:
            manager_radio.click()
            print("✓ Clic normal exitoso en rol Manager")
        except Exception:
            # Si falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", manager_radio)
            print("✓ Clic con JavaScript exitoso en rol Manager")

    except Exception as e:
        print(f"❌ Error al seleccionar rol Manager: {e}")

    # Paso 5: Hacer clic en "Add Instructor"
    print("Guardando instructor...")
    try:
        save_instructor_btn = wait.until(EC.element_to_be_clickable((By.ID, "btn-save-instructor-2")))

        # Hacer scroll al botón
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                              save_instructor_btn)
        time.sleep(1)

        # Intentar clic normal primero
        try:
            save_instructor_btn.click()
            print("✓ Clic normal exitoso en Add Instructor")
        except Exception:
            # Si falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", save_instructor_btn)
            print("✓ Clic con JavaScript exitoso en Add Instructor")

        print("✓ Instructor agregado exitosamente")

    except Exception as e:
        print(f"❌ Error al guardar instructor: {e}")

    # Esperar un momento para que se procesen los cambios
    time.sleep(3)
    print("--- PROCESO DE AGREGAR INSTRUCTOR COMPLETADO ---")

    input("Presiona ENTER para continuar y cerrar sesión...")

    # --- CERRAR SESIÓN ---
    profile_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'jcoronado@unsa.edu.pe')]")
    ))
    profile_button.click()

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
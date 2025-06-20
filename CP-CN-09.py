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

    # Esperar dentro de la sesión
    # print("Esperando 10 segundos...")
    # time.sleep(10)

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

    # === NUEVA FUNCIONALIDAD: ELIMINAR SESIÓN ===
    # Paso 3: Hacer clic en el botón Delete
    print("--- INICIANDO PROCESO DE ELIMINACIÓN DE SESIÓN ---")
    print("Preparando para hacer clic en Delete...")

    try:
        # Buscar todos los botones Delete disponibles
        print("Buscando todos los botones Delete disponibles...")

        # Buscar específicamente botones con clase btn-soft-delete-1
        delete_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'btn-soft-delete-1')]")

        if delete_buttons:
            print(f"Encontrados {len(delete_buttons)} botones Delete")

            # Por defecto, hacer clic en el primer botón Delete (sesión 1)
            # Si quieres cambiar cuál sesión eliminar, cambia el índice [0] por [1], [2], [3]
            delete_button = delete_buttons[0]  # Primera sesión (índice 0)

            print(f"Seleccionando botón Delete #{1} (primera sesión)")
            print(f"Clases del botón: {delete_button.get_attribute('class')}")
            print(f"Texto del botón: '{delete_button.text.strip()}'")
        else:
            # Si no encuentra con esa clase, buscar por otras estrategias
            print("No se encontraron botones con btn-soft-delete-1, probando otras estrategias...")

            # Buscar todos los botones que contengan "Delete"
            all_delete_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Delete')]")

            if all_delete_buttons:
                print(f"Encontrados {len(all_delete_buttons)} botones con texto 'Delete'")
                for i, btn in enumerate(all_delete_buttons):
                    print(f"  Botón {i + 1}: clases='{btn.get_attribute('class')}', texto='{btn.text.strip()}'")

                # Buscar el que tenga las clases correctas
                for btn in all_delete_buttons:
                    classes = btn.get_attribute('class')
                    if 'btn-light' in classes and 'btn-sm' in classes:
                        delete_button = btn
                        print(f"✓ Encontrado botón Delete con clases correctas: {classes}")
                        break
                else:
                    # Si no encuentra con clases específicas, tomar el primero
                    delete_button = all_delete_buttons[0]
                    print("Usando el primer botón Delete encontrado")
            else:
                raise Exception("No se encontró ningún botón Delete en la página")

        # Hacer scroll al elemento para asegurar que esté visible
        print("Haciendo scroll al botón Delete...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", delete_button)
        time.sleep(2)  # Dar tiempo para que termine el scroll

        # Intentar hacer clic normal primero
        try:
            # Esperar a que sea clickeable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(delete_button))
            delete_button.click()
            print("✓ Clic normal exitoso en Delete")
        except Exception:
            # Si el clic normal falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", delete_button)
            print("✓ Clic con JavaScript exitoso en Delete")

    except Exception as e:
        print(f"❌ Error al hacer clic en Delete: {e}")
        print("Tomando captura de pantalla para debug...")
        try:
            driver.save_screenshot("delete_button_error.png")
            print("Captura guardada como delete_button_error.png")
        except:
            pass
        input("PAUSA: Verifica manualmente y presiona ENTER...")

    # Dar tiempo para que aparezca la ventana modal de confirmación
    time.sleep(3)

    # Paso 4: Hacer clic en "Yes" en la ventana de confirmación
    print("Esperando ventana de confirmación...")
    print("Preparando para hacer clic en Yes...")

    try:
        # Buscar el botón "Yes" en la ventana modal
        yes_button = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             "//button[contains(@class, 'btn-warning') and contains(@class, 'modal-btn-ok') and contains(text(), 'Yes')]")
        ))

        # Hacer scroll si es necesario (aunque en modales generalmente no es necesario)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", yes_button)
        time.sleep(1)

        # Intentar clic normal primero
        try:
            yes_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[contains(@class, 'btn-warning') and contains(@class, 'modal-btn-ok') and contains(text(), 'Yes')]")
            ))
            yes_button.click()
            print("✓ Clic normal exitoso en Yes (confirmación)")
        except Exception:
            # Si falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", yes_button)
            print("✓ Clic con JavaScript exitoso en Yes (confirmación)")

        print("✓ Sesión eliminada exitosamente")

    except Exception as e:
        print(f"❌ Error al confirmar eliminación: {e}")
        input("PAUSA: Verifica manualmente y presiona ENTER...")

    # Esperar un momento para que se procesen los cambios
    time.sleep(3)
    print("--- PROCESO DE ELIMINACIÓN DE SESIÓN COMPLETADO ---")

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

    # input("Presiona ENTER para cerrar el navegador...")

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
#CP-CN-007
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

    # Hacer clic en el ícono de editar (fa-pen) - Múltiples estrategias
    print("Buscando ícono de editar...")

    try:
        # Estrategia 1: Buscar el botón padre que contiene el ícono
        edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//i[contains(@class, 'fa-pen')]]")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_button)
        time.sleep(2)
        edit_button.click()
        print("Se hizo clic en el botón de editar (Estrategia 1).")
    except:
        try:
            # Estrategia 2: Usar JavaScript para hacer clic en el ícono directamente
            edit_icon = driver.find_element(By.XPATH, "//i[contains(@class, 'fa-pen')]")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edit_icon)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", edit_icon)
            print("Se hizo clic en el ícono de editar (Estrategia 2 - JavaScript).")
        except:
            try:
                # Estrategia 3: Buscar por atributos más específicos
                edit_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                      "button[class*='btn'][aria-label*='edit'], button[title*='edit'], a[class*='btn'][aria-label*='edit']")))
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                      edit_element)
                time.sleep(2)
                edit_element.click()
                print("Se hizo clic en el elemento de editar (Estrategia 3).")
            except:
                # Estrategia 4: Última opción - buscar cualquier elemento clickeable que contenga fa-pen
                all_edit_elements = driver.find_elements(By.XPATH, "//*[.//i[contains(@class, 'fa-pen')]]")
                for element in all_edit_elements:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                              element)
                        time.sleep(1)
                        if element.is_displayed() and element.is_enabled():
                            driver.execute_script("arguments[0].click();", element)
                            print("Se hizo clic en el elemento de editar (Estrategia 4).")
                            break
                    except:
                        continue

    # Esperar a que aparezca el campo de input y escribir "curso editato"
    print("Esperando campo de input para editar nombre...")
    course_name_input = wait.until(EC.element_to_be_clickable((By.ID, "course-name")))

    # Limpiar el campo y escribir el nuevo nombre
    course_name_input.clear()
    course_name_input.send_keys("curso editato 3")
    print("Se escribió 'curso editato' en el campo de nombre del curso.")

    # Hacer clic en el botón "Save Changes" - Múltiples estrategias
    print("Buscando botón 'Save Changes'...")

    try:
        # Estrategia 1: Scroll más inteligente y JavaScript click
        save_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-save-course")))

        # Scroll para evitar la navbar fija (más hacia abajo del centro)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_button)
        time.sleep(2)

        # Hacer scroll adicional hacia abajo para alejar el botón de la navbar
        driver.execute_script("window.scrollBy(0, -150);")
        time.sleep(1)

        # Usar JavaScript click para evitar interceptación
        driver.execute_script("arguments[0].click();", save_button)
        print("Se hizo clic en 'Save Changes' (Estrategia 1 - JavaScript).")

    except:
        try:
            # Estrategia 2: Enviar el formulario directamente
            save_button = driver.find_element(By.ID, "btn-save-course")
            form = save_button.find_element(By.XPATH, "./ancestor::form")
            driver.execute_script("arguments[0].submit();", form)
            print("Formulario enviado directamente (Estrategia 2 - Submit).")

        except:
            try:
                # Estrategia 3: Simular Enter en el campo de texto
                course_name_input = driver.find_element(By.ID, "course-name")
                course_name_input.send_keys(Keys.ENTER)
                print("Cambios guardados con ENTER (Estrategia 3).")

            except:
                try:
                    # Estrategia 4: Maximizar ventana y reintentar
                    driver.maximize_window()
                    time.sleep(1)
                    save_button = driver.find_element(By.ID, "btn-save-course")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});",
                                          save_button)
                    time.sleep(2)
                    driver.execute_script("arguments[0].click();", save_button)
                    print("Se hizo clic en 'Save Changes' (Estrategia 4 - Ventana maximizada).")

                except Exception as e:
                    print(f"No se pudo hacer clic en Save Changes: {e}")
                    print("Intentando buscar cualquier botón de guardar...")

                    # Estrategia 5: Buscar cualquier botón que contenga "Save"
                    save_buttons = driver.find_elements(By.XPATH,
                                                        "//button[contains(text(), 'Save') or contains(@value, 'Save')]")
                    for btn in save_buttons:
                        try:
                            driver.execute_script("arguments[0].click();", btn)
                            print("Se encontró y clickeó un botón de guardar alternativo.")
                            break
                        except:
                            continue

    # Esperar un momento para que se procesen los cambios
    time.sleep(3)
    print("Proceso de guardado completado.")

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
    print(f"Ocurrió un error: {e}")

finally:
    driver.quit()
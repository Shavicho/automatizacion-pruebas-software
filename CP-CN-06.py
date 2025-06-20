#CP-CN-015
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

    # Paso 3: Hacer clic en Add New Question
    print("Preparando para hacer clic en Add New Question...")

    try:
        # Buscar el elemento primero
        add_question_button = wait.until(EC.presence_of_element_located((By.ID, "btn-new-question")))

        # Hacer scroll al elemento para asegurar que esté visible
        print("Haciendo scroll al botón...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                              add_question_button)
        time.sleep(2)  # Dar tiempo para que termine el scroll

        # Intentar hacer clic normal primero
        try:
            add_question_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-new-question")))
            add_question_button.click()
            print("✓ Clic normal exitoso en Add New Question")
        except Exception:
            # Si el clic normal falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", add_question_button)
            print("✓ Clic con JavaScript exitoso en Add New Question")

    except Exception as e:
        print(f" Error al hacer clic en Add New Question: {e}")
        input("PAUSA: Verifica manualmente y presiona ENTER...")

    # Dar tiempo para que aparezca el dropdown
    time.sleep(2)

    # Paso 4: Hacer clic en "Multiple-choice (multiple answers) question"
    print("Preparando para seleccionar Multiple-choice...")

    try:
        # Buscar el botón del dropdown
        multiple_choice_button = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             "//button[contains(@class, 'dropdown-item') and contains(text(), 'Multiple-choice (multiple answers) question')]")
        ))

        # Hacer scroll si es necesario
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                              multiple_choice_button)
        time.sleep(1)

        # Intentar clic normal primero
        try:
            multiple_choice_button.click()
            print("✓ Clic normal exitoso en Multiple-choice")
        except Exception:
            # Si falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", multiple_choice_button)
            print("✓ Clic con JavaScript exitoso en Multiple-choice")

    except Exception as e:
        print(f" Error al seleccionar Multiple-choice: {e}")
        input("PAUSA: Verifica manualmente y presiona ENTER...")

    # Paso 5: Escribir en el campo de pregunta
    print("Esperando a que aparezca el campo de pregunta...")
    time.sleep(5)  # Aumentar tiempo de espera

    try:
        # Buscar el textarea visible y disponible para interacción
        print("Buscando el elemento textarea correcto...")

        # Opción 1: Buscar el que tenga la clase 'ng-valid' (el último/activo)
        try:
            question_field = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@id='question-brief' and contains(@class, 'ng-valid')]")
            ))
            print("✓ Elemento encontrado con clase ng-valid!")
        except TimeoutException:
            # Opción 2: Buscar todos los elementos y tomar el último visible
            print("Probando con el último elemento visible...")
            elements = driver.find_elements(By.ID, "question-brief")
            question_field = None
            for elem in reversed(elements):  # Probar desde el último hacia atrás
                try:
                    if elem.is_displayed() and elem.is_enabled():
                        question_field = elem
                        print(f"✓ Elemento encontrado: {elem.get_attribute('class')}")
                        break
                except:
                    continue

            if question_field is None:
                raise Exception("No se pudo encontrar un elemento question-brief clickeable")

        # Escribir texto
        print("Limpiando campo...")
        question_field.clear()
        print("Escribiendo texto...")
        question_field.send_keys("esta es una pregunta de prueba")
        print("✓ Texto escrito correctamente!")

    except TimeoutException as e:
        print(f" Timeout al buscar el campo de pregunta: {e}")
        input("PAUSA: Presiona ENTER para continuar con error...")

    except Exception as e:
        print(f" Error inesperado: {type(e).__name__}: {e}")
        input("PAUSA: Presiona ENTER para continuar con error...")

    else:
        # Solo continuar con el resto si no hubo errores
        print("Continuando con el resto del proceso...")

        # Paso 6: Hacer clic en "Add More Options" 2 veces
        try:
            for i in range(2):
                add_option_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-add-option")))

                # Hacer scroll al botón
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                      add_option_button)
                time.sleep(1)

                # Intentar clic
                try:
                    add_option_button.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", add_option_button)

                print(f"✓ Add More Options clic {i + 1}/2")
                time.sleep(1)  # Pausa entre clics
        except Exception as e:
            print(f" Error en Add More Options: {e}")

        # Paso 7: Escribir en todas las opciones disponibles
        try:
            print("Escribiendo en todas las opciones...")
            time.sleep(2)  # Dar tiempo para que aparezcan todos los campos

            # Buscar todos los campos de opción
            option_inputs = driver.find_elements(
                By.XPATH, "//input[@type='text' and @aria-label='Option' and contains(@class, 'form-control')]"
            )

            print(f"Encontrados {len(option_inputs)} campos de opción")

            # Texto para cada opción
            option_texts = ["Opcion 1", "Opcion 2", "Opcion 3", "Opcion 4"]

            # Llenar cada campo de opción
            for i, option_input in enumerate(option_inputs):
                if i < len(option_texts):  # Asegurarse de no exceder los textos disponibles
                    try:
                        # Hacer scroll al campo
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                              option_input)
                        time.sleep(0.5)

                        # Limpiar y escribir
                        option_input.clear()
                        option_input.send_keys(option_texts[i])
                        print(f"✓ Escrito '{option_texts[i]}' en campo {i + 1}")

                    except Exception as e:
                        print(f" Error al escribir en opción {i + 1}: {e}")

        except Exception as e:
            print(f" Error general al escribir opciones: {e}")

        # Paso 8: Hacer clic en "Save Question"
        try:
            save_question_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-save-new")))

            # Hacer scroll al botón
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                  save_question_button)
            time.sleep(1)

            # Intentar clic
            try:
                save_question_button.click()
            except Exception:
                driver.execute_script("arguments[0].click();", save_question_button)

            print("✓ Pregunta guardada exitosamente")
        except Exception as e:
            print(f" Error al guardar pregunta: {e}")

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

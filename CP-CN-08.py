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
    time.sleep(5)

    # === NUEVA FUNCIONALIDAD: EDITAR TINYMCE ===
    print("--- INICIANDO PROCESO DE EDICIÓN DE TINYMCE ---")

    try:
        # Buscar el iframe de TinyMCE
        print("Buscando iframe de TinyMCE...")

        # Buscar iframe por clase o título
        tinymce_iframe = None

        # Estrategia 1: Buscar por clase tox-edit-area__iframe
        try:
            tinymce_iframe = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "tox-edit-area__iframe")
            ))
            print("✓ Iframe encontrado por clase tox-edit-area__iframe")
        except TimeoutException:
            # Estrategia 2: Buscar por título "Rich Text Area"
            try:
                tinymce_iframe = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//iframe[@title='Rich Text Area']")
                ))
                print("✓ Iframe encontrado por título 'Rich Text Area'")
            except TimeoutException:
                # Estrategia 3: Buscar cualquier iframe que contenga 'tiny' en el ID
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    iframe_id = iframe.get_attribute("id")
                    if iframe_id and "tiny" in iframe_id.lower():
                        tinymce_iframe = iframe
                        print(f"✓ Iframe encontrado por ID: {iframe_id}")
                        break

                if tinymce_iframe is None:
                    raise Exception("No se pudo encontrar el iframe de TinyMCE")

        # Hacer scroll al iframe
        print("Haciendo scroll al iframe...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", tinymce_iframe)
        time.sleep(2)

        # Cambiar al contexto del iframe
        print("Cambiando al contexto del iframe...")
        driver.switch_to.frame(tinymce_iframe)

        # Buscar el elemento editable dentro del iframe
        print("Buscando elemento editable...")
        try:
            # Buscar el body con contenteditable="true"
            editable_body = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//body[@contenteditable='true']")
            ))
            print("✓ Elemento editable encontrado")
        except TimeoutException:
            # Alternativa: buscar por ID tinymce
            try:
                editable_body = wait.until(EC.element_to_be_clickable(
                    (By.ID, "tinymce")
                ))
                print("✓ Elemento editable encontrado por ID")
            except TimeoutException:
                # Última alternativa: buscar cualquier elemento contenteditable
                editable_body = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@contenteditable='true']")
                ))
                print("✓ Elemento editable encontrado genérico")

        # Hacer clic en el elemento para activarlo
        print("Activando el editor...")
        editable_body.click()
        time.sleep(1)

        # Limpiar todo el contenido
        print("Limpiando contenido anterior...")
        driver.execute_script("arguments[0].innerHTML = '';", editable_body)

        # Escribir el nuevo contenido
        print("Escribiendo nuevo contenido...")
        new_content = "editando automaticamente"
        driver.execute_script(f"arguments[0].innerHTML = '<p>{new_content}</p>';", editable_body)

        # Alternativa con send_keys si lo anterior no funciona
        try:
            # Limpiar con Ctrl+A y Delete
            editable_body.clear()
            editable_body.send_keys(new_content)
        except:
            pass  # Si falla, ya lo hicimos con JavaScript

        print("✓ Contenido editado exitosamente")

        # Hacer clic fuera del editor para guardar cambios
        print("Guardando cambios...")
        driver.execute_script("arguments[0].blur();", editable_body)

        # Volver al contexto principal
        print("Volviendo al contexto principal...")
        driver.switch_to.default_content()

        print("✓ Edición de TinyMCE completada exitosamente")

    except Exception as e:
        print(f"❌ Error al editar TinyMCE: {e}")
        # Asegurarse de volver al contexto principal en caso de error
        try:
            driver.switch_to.default_content()
        except:
            pass

        # Tomar captura de pantalla para debug
        try:
            driver.save_screenshot("tinymce_edit_error.png")
            print("Captura guardada como tinymce_edit_error.png")
        except:
            pass

        input("PAUSA: Verifica manualmente y presiona ENTER...")

    print("--- PROCESO DE EDICIÓN DE TINYMCE COMPLETADO ---")

    # === FUNCIONALIDAD ADICIONAL: MODIFICAR SELECT Y FECHA ===
    print("--- INICIANDO MODIFICACIONES ADICIONALES ---")

    try:
        # Paso 1: Modificar el select de Grace Period
        print("Modificando Grace Period...")

        # Buscar el select por ID
        grace_period_select = wait.until(EC.element_to_be_clickable((By.ID, "grace-period")))

        # Hacer scroll al elemento
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                              grace_period_select)
        time.sleep(1)

        # Obtener el valor actual
        current_value = grace_period_select.get_attribute("value")
        print(f"Valor actual del Grace Period: {current_value}")

        # Lógica condicional: si está en 25, cambiar a 10; si no, cambiar a 25
        from selenium.webdriver.support.ui import Select

        select = Select(grace_period_select)

        # Obtener el texto de la opción seleccionada
        current_text = select.first_selected_option.text
        print(f"Opción actual: {current_text}")

        if "25" in current_text:
            # Si está en 25 min, cambiar a 10 min
            select.select_by_visible_text("10 min")
            print("✓ Cambiado de 25 min a 10 min")
        else:
            # Si está en cualquier otra opción, cambiar a 25 min
            select.select_by_visible_text("25 min")
            print("✓ Cambiado a 25 min")

        time.sleep(1)

    except Exception as e:
        print(f"❌ Error al modificar Grace Period: {e}")

    try:
        # Paso 2: Buscar y modificar campos de fecha
        print("Buscando campos de fecha...")

        # Buscar botones que abran el datepicker (calendario)
        calendar_buttons = driver.find_elements(By.XPATH,
                                                "//button[contains(@class, 'calendar') or contains(@aria-label, 'calendar') or contains(@title, 'calendar')]")

        # También buscar botones con íconos de calendario
        if not calendar_buttons:
            calendar_buttons = driver.find_elements(By.XPATH,
                                                    "//button[contains(@class, 'fa-calendar') or .//i[contains(@class, 'fa-calendar')] or .//span[contains(@class, 'calendar')]]")

        # Buscar cualquier botón cerca de inputs de fecha
        if not calendar_buttons:
            calendar_buttons = driver.find_elements(By.XPATH,
                                                    "//div[contains(@class, 'input-group')]//button")

        if calendar_buttons:
            print(f"Encontrados {len(calendar_buttons)} botones de calendario")

            # Hacer clic en el primer botón de calendario
            try:
                calendar_button = calendar_buttons[0]
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                      calendar_button)
                time.sleep(1)

                calendar_button.click()
                print("✓ Botón de calendario clickeado")

                # Esperar a que aparezca el datepicker
                time.sleep(3)

                # Buscar el datepicker de Angular Bootstrap
                try:
                    # Estrategia 1: Buscar el día actual (ngb-dp-today)
                    today_element = driver.find_element(By.XPATH, "//div[contains(@class, 'ngb-dp-today')]")
                    print("✓ Encontrado elemento 'hoy' en el datepicker")

                    # Hacer clic en el día actual
                    today_element.click()
                    print("✓ Fecha actual seleccionada")

                except Exception:
                    # Estrategia 2: Buscar el botón "Hoy" al final del datepicker
                    try:
                        today_button = driver.find_element(By.XPATH,
                                                           "//button[contains(text(), 'Hoy') or contains(text(), 'Today')]")
                        today_button.click()
                        print("✓ Botón 'Hoy' clickeado")

                    except Exception:
                        # Estrategia 3: Seleccionar cualquier día disponible (no disabled)
                        try:
                            available_days = driver.find_elements(By.XPATH,
                                                                  "//div[contains(@class, 'ngb-dp-day') and not(contains(@class, 'disabled'))]")

                            if available_days:
                                # Obtener el día actual del mes
                                from datetime import datetime

                                current_day = datetime.now().day

                                # Buscar el día actual específicamente
                                for day in available_days:
                                    day_text = day.text.strip()
                                    if day_text == str(current_day):
                                        day.click()
                                        print(f"✓ Día actual ({current_day}) seleccionado")
                                        break
                                else:
                                    # Si no encuentra el día actual, hacer clic en el primer día disponible
                                    available_days[0].click()
                                    print("✓ Primer día disponible seleccionado")

                        except Exception as e:
                            print(f"❌ No se pudo seleccionar fecha en datepicker: {e}")

                # Pequeña pausa para que se cierre el datepicker
                time.sleep(1)

            except Exception as e:
                print(f"❌ Error al manejar calendario: {e}")

        # Intentar también con el select de horas si está disponible
        try:
            print("Buscando select de horas...")
            hour_selects = driver.find_elements(By.XPATH,
                                                "//select[contains(@aria-label, 'hora') or contains(@aria-label, 'hour')]")

            if hour_selects:
                hour_select = hour_selects[0]

                # Verificar si tiene opciones no deshabilitadas
                from selenium.webdriver.support.ui import Select

                select = Select(hour_select)
                available_options = [opt for opt in select.options if not opt.get_attribute("disabled")]

                if available_options:
                    print(f"Encontradas {len(available_options)} opciones de hora disponibles")
                    # Seleccionar una hora disponible (por ejemplo, la primera)
                    select.select_by_index(0)
                    print("✓ Hora seleccionada")
                else:
                    print("Todas las opciones de hora están deshabilitadas")
            else:
                print("No se encontraron selectores de hora")

        except Exception as e:
            print(f"❌ Error al manejar selector de horas: {e}")

        if not calendar_buttons:
            print("No se encontraron botones de calendario visibles")

    except Exception as e:
        print(f"❌ Error general al buscar fechas: {e}")

    try:
        # Paso 3: Hacer clic en "Save Changes"
        print("Buscando botón Save Changes...")

        # Buscar el botón Save Changes
        save_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'btn-success') and contains(text(), 'Save Changes')]")
        ))

        # Hacer scroll al botón
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_button)
        time.sleep(1)

        # Intentar clic normal primero
        try:
            save_button.click()
            print("✓ Clic normal exitoso en Save Changes")
        except Exception:
            # Si falla, usar JavaScript
            print("Clic normal falló, usando JavaScript...")
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Clic con JavaScript exitoso en Save Changes")

        print("✓ Cambios guardados exitosamente")

    except Exception as e:
        print(f"❌ Error al hacer clic en Save Changes: {e}")

    print("--- MODIFICACIONES ADICIONALES COMPLETADAS ---")

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

    # Asegurarse de volver al contexto principal
    try:
        driver.switch_to.default_content()
    except:
        pass

    # Intentar tomar una captura de pantalla para debug
    try:
        driver.save_screenshot("error_screenshot.png")
        print("Captura de pantalla guardada como error_screenshot.png")
    except:
        pass

    input("Presiona ENTER para continuar con el debug...")

finally:
    driver.quit()
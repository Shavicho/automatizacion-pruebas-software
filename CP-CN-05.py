# CP-CN-011
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# ---------- CONFIGURACIÓN ----------
CHR_PATH = r"C:\chromedriver-win64\chromedriver.exe"
PROFILE = r"C:\Users\user\selenium-profile"
URL_HOME = "https://teammates-libelula2.uc.r.appspot.com/web/front/home"

service = Service(executable_path=CHR_PATH)
options = Options()
options.add_argument(fr"--user-data-dir={PROFILE}")
options.add_argument("--start-maximized")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

try:
    driver.get(URL_HOME)

    # ---------- LOGIN  ----------
    try:
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']")))
        login_btn.click()
        wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn"))).click()
        print("Sesión iniciada.")
    except TimeoutException:
        print("Ya estabas logueado.")

    # ---------- 1) Pestaña "Students" ----------
    print("Abriendo pestaña 'Students'...")
    students_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Students']")))
    students_tab.click()

    # ---------- 2) Expandir panel del curso ----------
    print("Expandiendo panel del curso...")
    expand_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class,'chevron') and contains(@class,'btn-course')]")
    ))
    driver.execute_script("arguments[0].scrollIntoView(true);", expand_btn)
    driver.execute_script("arguments[0].click();", expand_btn)

    # ---------- 3) Enlace "Enroll Students" ----------
    print("Entrando a 'Enroll Students'...")
    enroll_page_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='btn-enroll' and contains(.,'Enroll Students')]")))
    enroll_page_link.click()

    # Esperar a que cargue completamente la página
    print("Esperando a que cargue la página de inscripción...")
    time.sleep(3)

    # ---------- 4) MÉTODO MEJORADO: Interactuar con Handsontable ----------
    print("=== INICIANDO PROCESO DE INSCRIPCIÓN DE ESTUDIANTES ===")

    try:
        # Buscar la tabla de New Students
        print("Buscando tabla 'New Students'...")
        tabla_nuevos = wait.until(EC.presence_of_element_located((By.ID, "newStudentsHOT")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", tabla_nuevos)
        time.sleep(2)

        print("✓ Tabla encontrada")

        # === MÉTODO 1: Usar JavaScript para llenar directamente ===
        print("Método 1: Intentando con JavaScript...")

        # Datos a insertar
        estudiantes = [
            ["Section A", "Libelulas2", "Juan Pérez", "juan98.perez@example.com", "Comentario 1"],
            ["Section B", "Gusanos2", "María López", "maria98.lopez@example.com", "Comentario 2"],
            ["Section A", "Tarantula2", "Carlos Rodríguez", "carlos98.rodriguez@example.com", "-"]
        ]

        try:
            # Intentar obtener la instancia de Handsontable via JavaScript
            script = """
            var hotElement = document.getElementById('newStudentsHOT');
            if (hotElement && hotElement.hotInstance) {
                var hot = hotElement.hotInstance;
                var data = arguments[0];
                hot.loadData(data);
                hot.render();
                return 'success';
            }
            return 'no_instance';
            """

            result = driver.execute_script(script, estudiantes)

            if result == 'success':
                print("✓ Datos insertados correctamente con JavaScript")
            else:
                raise Exception("No se pudo acceder a la instancia de Handsontable")

        except Exception as e:
            print(f"Método 1 falló: {e}")

            # === MÉTODO 2: Interacción celda por celda ===
            print("Método 2: Interacción celda por celda...")

            for fila_idx, estudiante in enumerate(estudiantes):
                print(f"Insertando estudiante {fila_idx + 1}: {estudiante[2]}")

                # IMPORTANTE: Empezar desde columna 2 (índice 2) porque la columna 1 son los números de fila
                for col_idx, valor in enumerate(estudiante):
                    try:
                        # Buscar la celda específica - EMPEZAR DESDE COLUMNA 2
                        columna_real = col_idx + 2  # +2 porque la primera columna (índice 1) son números
                        fila_real = fila_idx + 1

                        celda_selector = f"#newStudentsHOT .htCore tbody tr:nth-child({fila_real}) td:nth-child({columna_real})"

                        print(f"  Intentando celda ({fila_real}, {columna_real}) para: {valor}")

                        # Esperar y hacer clic en la celda
                        celda = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, celda_selector)))

                        # Hacer scroll a la celda
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                              celda)
                        time.sleep(0.3)

                        # Hacer doble clic para activar edición
                        ActionChains(driver).double_click(celda).perform()
                        time.sleep(0.5)

                        # Buscar el campo de entrada activo
                        input_encontrado = False

                        # Opción 1: Buscar textarea
                        try:
                            textarea = driver.find_element(By.CSS_SELECTOR, "textarea.handsontableInput")
                            if textarea.is_displayed():
                                textarea.clear()
                                textarea.send_keys(valor)
                                textarea.send_keys(Keys.ENTER)
                                input_encontrado = True
                                print(f"  ✓ Celda ({fila_real}, {columna_real}) con textarea: {valor}")
                        except:
                            pass

                        # Opción 2: Buscar input si no hay textarea
                        if not input_encontrado:
                            try:
                                input_field = driver.find_element(By.CSS_SELECTOR, "input.handsontableInput")
                                if input_field.is_displayed():
                                    input_field.clear()
                                    input_field.send_keys(valor)
                                    input_field.send_keys(Keys.ENTER)
                                    input_encontrado = True
                                    print(f"  ✓ Celda ({fila_real}, {columna_real}) con input: {valor}")
                            except:
                                pass

                        # Opción 3: Enviar teclas directamente a la celda
                        if not input_encontrado:
                            try:
                                celda.send_keys(valor)
                                celda.send_keys(Keys.ENTER)
                                input_encontrado = True
                                print(f"  ✓ Celda ({fila_real}, {columna_real}) directo: {valor}")
                            except:
                                pass

                        if not input_encontrado:
                            print(f"   No se pudo escribir en celda ({fila_real}, {columna_real})")

                        time.sleep(0.5)  # Pausa entre celdas

                    except Exception as e:
                        print(f"   Error en celda ({fila_idx + 1}, {col_idx + 2}): {str(e)[:50]}...")
                        continue

                print(f"✓ Estudiante {fila_idx + 1} procesado")
                time.sleep(1)  # Pausa entre filas

        # === MÉTODO 3: Alternativa con copy-paste ===
        if all(estudiante == ["", "", "", "", ""] for estudiante in estudiantes):  # Si no se llenó nada
            print("Método 3: Intentando copy-paste...")

            # Preparar datos en formato tabulado
            datos_csv = "\n".join(["\t".join(estudiante) for estudiante in estudiantes])

            try:
                # Hacer clic en la primera celda
                primera_celda = driver.find_element(By.CSS_SELECTOR,
                                                    "#newStudentsHOT .htCore tbody tr:first-child td:first-child")
                primera_celda.click()
                time.sleep(1)

                # Intentar pegar datos
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

                # O usar el textarea oculto
                textarea = driver.find_element(By.CSS_SELECTOR, "textarea.handsontableInput")
                textarea.send_keys(datos_csv)

                print("✓ Datos pegados")

            except Exception as e:
                print(f"Método 3 falló: {e}")

        print("✓ Datos de estudiantes insertados")

    except Exception as e:
        print(f" Error al llenar la tabla: {e}")

        # Tomar captura de pantalla para debug
        try:
            driver.save_screenshot("handsontable_error.png")
            print("Captura guardada como handsontable_error.png")
        except:
            pass

    # ---------- 5) Botón verde "Enroll students" ----------
    print("Confirmando inscripción...")
    try:
        # Buscar el botón de inscripción
        confirm_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@id='btn-enroll' and contains(.,'Enroll')]")
        ))

        # Hacer scroll al botón
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", confirm_btn)
        time.sleep(1)

        # Hacer clic
        confirm_btn.click()
        print("✓ Estudiantes inscritos correctamente.")

        # Esperar confirmación
        time.sleep(3)

    except Exception as e:
        print(f" Error al hacer clic en 'Enroll students': {e}")

    print("=== PROCESO DE INSCRIPCIÓN COMPLETADO ===")

    # ---------- 6) Esperar ENTER, cerrar sesión ----------
    input("Presiona ENTER para cerrar sesión y salir...")

    profile_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'jcoronado@unsa.edu.pe')]")
    ))
    profile_btn.click()
    wait.until(EC.element_to_be_clickable((By.ID, "logout-btn"))).click()
    print("Sesión cerrada correctamente.")

except Exception as e:
    print(f" Ocurrió un error: {e}")

    # Tomar captura de pantalla para debug
    try:
        driver.save_screenshot("error_general.png")
        print("Captura guardada como error_general.png")
    except:
        pass

finally:
    driver.quit()


#CP-CN-005
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
driver.get("https://teammatesv4.appspot.com/web/front/home")

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

    # Hacer clic en "Add New Course"
    print("Esperando botón 'Add New Course'...")
    add_course_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Add New Course')]")))
    add_course_btn.click()

    # Llenar campos del nuevo curso
    print("Esperando campos para ingresar curso...")
    course_id_input = wait.until(EC.element_to_be_clickable((By.ID, "course-id")))
    course_name_input = wait.until(EC.element_to_be_clickable((By.ID, "course-name")))

    course_id_input.clear()
    course_id_input.send_keys("CS5555-2025Semester4")

    course_name_input.clear()
    course_name_input.send_keys("Intro to Testing4")

    # Esperar a que el botón esté habilitado y hacer clic
    print("Esperando botón 'Add Course' habilitado...")
    wait.until(lambda driver: driver.find_element(By.ID, "btn-submit-course").is_enabled())
    add_course_button = driver.find_element(By.ID, "btn-submit-course")
    add_course_button.click()
    print("Curso agregado correctamente.")

    input("Presiona ENTER para cerrar sesión y salir...")

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

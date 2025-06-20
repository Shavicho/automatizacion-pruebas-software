#CP-CN-006
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

    # Hacer clic en el botón "Archive"
    print("Esperando botón 'Archive'...")
    archive_btn = wait.until(EC.element_to_be_clickable((By.ID, "btn-archive-0")))
    archive_btn.click()
    print("Curso archivado correctamente.")

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

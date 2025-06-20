#CP-CN-01
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
    #print("Esperando 10 segundos...")
    #time.sleep(10)

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

    #input("Presiona ENTER para cerrar el navegador...")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    driver.quit()

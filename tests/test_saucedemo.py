import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import  Service
from webdriver_manager.chrome import  ChromeDriverManager
from selenium.webdriver.common.by import By
from utils.helpers import login_helper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module") #scope="function"
def driver():

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()



def test_01_login(driver):

    login_helper(driver, "standard_user", "secret_sauce")
    assert "/inventory.html" in driver.current_url, "ERROR: No se redirigio a /inventory.html"


def test_02_verificar_inventario(driver):
    section_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    ).text

    assert driver.title == "Swag Labs"
    assert section_title == "Products"


def test_03_productos_visibles(driver):

    inventory_item = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    assert len(inventory_item) > 0 , f'ERROR: No se encontraron productos visibles'

    

def test_04_validad_interfaz( driver ):

    menu_button = driver.find_element(By.ID, 'react-burger-menu-btn')
    filtro = driver.find_element(By.CLASS_NAME, 'product_sort_container')

    assert menu_button.is_displayed(), f'ERROR: Menu no esta visible'
    assert filtro.is_displayed(), f'ERROR: filtro no esta visible'




def test_05_añadir_producto_al_carrito(driver):
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    boton_remove = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "remove-sauce-labs-backpack")
        )
    )

    assert boton_remove.text == "Remove"


def test_06_verificar_contador_carrito( driver ):

    contador_carrito = driver.find_element(By.CLASS_NAME,'shopping_cart_badge').text

    assert contador_carrito == "1" ,f'ERROR: Se esperaba 1 , obtuvo {contador_carrito}'


def test_07_navegar_carrito(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/cart.html")
    )

    assert "/cart.html" in driver.current_url




def test_08_comprobar_producto_en_el_carrito( driver):

    assert "/cart.html" in driver.current_url, "ERROR: No estás en el carrito"
    
    producto_nombre_en_carrito = driver.find_element(By.CLASS_NAME, 'inventory_item_name').text

    assert producto_nombre_en_carrito == 'Sauce Labs Backpack' , f'ERROR: NO ES EL MISMO NOMBRE'
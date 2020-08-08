import logging, time, psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command as comm
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)

weburl = 'http://127.0.0.1:8000/'

# mobile_emulation = { "deviceName": "iPhone 5" }
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome('C:/Program Files (x86)/Google/chromedriver_selenium/chromedriver.exe') # ,  desired_capabilities = chrome_options.to_capabilities())
# driver = webdriver.Edge()


# driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities = chrome_options.to_capabilities())

def start_setup():
    # pasar esta funcion una vez , solo al inicio.
    val_jor= str(55)
    porcentaje = 50
    ini_work = "00"+"2020-01-20T18:00"
    end_work = "00"+"2020-01-21T18:00"
    hs_por_jor = 12
    nocturno = False
    driver.get(weburl)
    driver.set_window_position(55, 55)
    driver.set_window_size(1100, 900)

    # WebDriverWait(driver, 1)
    # try:
    #     # WebDriverWait(2,4)
    #     driver.find_element_by_name('fee_in').send_keys(val_jor)
    #     # driver.find_element_by_name('start_work').send_keys(Keys.CLEAR)
    #     driver.find_element_by_name('start_work').send_keys(ini_work)
    #     # driver.find_element_by_name('end_work').send_keys(Keys.CLEAR)
    #     driver.find_element_by_name('end_work').send_keys(end_work)
    #     # driver.find_element_by_name('Calcular Total').click()
    # except Exception:
    #     print(Exception)
    #     pass
    try:
        if driver.find_element_by_name('fee_in').get_attribute('value') != val_jor:
            driver.find_element_by_name('fee_in').send_keys(Keys.CONTROL + 'a')
            driver.find_element_by_name('fee_in').send_keys(Keys.CLEAR)
            # print(driver.find_element_by_name('fee_in').get_attribute('value') )
            driver.find_element_by_name('fee_in').send_keys(val_jor)
            print(f'el costo por jornada se fijo en == {val_jor}')
        driver.find_element_by_name('start_work').send_keys(Keys.CLEAR)
        driver.find_element_by_name('start_work').send_keys(ini_work)
        driver.find_element_by_name('end_work').send_keys(Keys.CLEAR)
        driver.find_element_by_name('end_work').send_keys(end_work)
        driver.find_element_by_name('noc_chk').click() if nocturno == True else driver.find_element_by_name('noc_chk').click() if driver.find_element_by_name('noc_chk').get_attribute("checked") else print('el horario nocturno será deschequeado')
    except Exception:
        pass

def loop_refresh(refresh_time=10):
    rft = refresh_time
    logging.info(f'\nNOTE: The web browser will be refreshed at {rft}\" intervals ')

    while True:
        time.sleep(rft)
        # driver.implicitly_wait(rft)
        try:
            WebDriverWait(driver, 1).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(alert.text)
            # alert.accept()
            alert.dismiss()
            print("alert accepted")
        except Exception:
            if psutil.Process(driver.service.process.pid).is_running():
                driver.refresh()
                t = time.localtime()
                logging.info(f'\n--- refreshing the web: {weburl} at {time.strftime("%H:%M:%S" , t)}')
                # driver.find_element_by_name('Calcular Total').click() # temp for test
                ## Double check for avoid empty values when selenium can't fill every data fields.
                if len(driver.find_element_by_name('start_work').get_attribute('value')) == 0:
                    logging.info('\nrestarting the setup for refill data')
                    start_setup()
                driver.find_element_by_name('Calcular Total').click() # temp for test
            else:
                driver.close()
                driver.quit()
        except:
            if driver.find_element_by_id("PageUnavailable"):
                logging.info('page needs to be refreshed \n')
                driver.implicitly_wait(1)
                driver.refresh()



if __name__ == '__main__':
    start_setup()
    loop_refresh(3)

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3


def module_test_seeds():

    try:

        def wait_until_xpath(wait, xpath):
            return wait.until(lambda d: d.find_element(by=By.XPATH, value=xpath))

        def wait_until_xpath_and_click(wait, xpath):
            wait_until_xpath(wait, xpath).click()

        def wait_until_xpath_and_send_keys(wait, xpath, keys):
            element = wait_until_xpath(wait, xpath)
            element.send_keys(keys)
            return element

        driver = webdriver.Firefox(
            executable_path=r"C:\Users\crypt\Desktop\MetaBot_vF\geckodriver.exe"
        )
        wait = WebDriverWait(driver, 5)
        original_window = driver.current_window_handle
        extension_path = (
            "C:\\Users\crypt\Desktop\MetaBot_vF\webextension@metamask.io.xpi"
        )
        driver.install_addon(extension_path, temporary=True)
        wait.until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        time.sleep(3)
        driver.refresh()

        elements = wait.until(lambda d: d.find_elements(By.TAG_NAME, "button"))
        get_started = elements[0]
        get_started.click()
        wait_until_xpath_and_click(wait, "// button[contains(text(),'Import wallet')]")
        wait_until_xpath_and_click(wait, "// button[contains(text(),'I Agree')]")

        connexionBDD = sqlite3.connect(r"C:\Users\crypt\Desktop\MetaBot_vF\MetaBDD.db")
        curseur = connexionBDD.cursor()
        chercher_seed = curseur.execute(
            "SELECT * FROM MetaBDDTable WHERE statutSeed = 'untested'"
        )
        ajout_iteration = "UPDATE MetaBDDTable SET statutSeed = ? WHERE seedId = ?"
        curseur_update = connexionBDD.cursor()

        for seed in chercher_seed:
            seed_testee = seed[1]
            seed_id_testee = seed[0]
            send_input = wait_until_xpath_and_send_keys(
                wait,
                "/html/body/div[1]/div/div[2]/div/div/form/div[4]/div[1]/div/input",
                seed_testee,
            )

            try:
                driver.find_element(
                    by=By.XPATH,
                    value="/html/body/div[1]/div/div[2]/div/div/form/div[4]/span",
                )
                colonne_status = ("INVALIDE", seed_id_testee)
                print("Seed invalide")
            except:
                colonne_status = ("VALIDE", seed_id_testee)
                print("Seed valide")
            curseur_update.execute(ajout_iteration, colonne_status)
            connexionBDD.commit()
            send_input.clear()
        connexionBDD.close()
        driver.quit()
        return 1
    except:
        connexionBDD.close()
        driver.quit()
        return 0

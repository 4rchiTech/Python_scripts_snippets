from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3


def module_extraction_adresses():

    try:

        driver = webdriver.Firefox(
            executable_path=r"C:\Users\crypt\Desktop\MetaBot_vF\geckodriver.exe"
        )
        original_window = driver.current_window_handle
        wait = WebDriverWait(driver, 5)
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
        element_import_wallet = wait.until(
            lambda d: d.find_element_by_xpath(
                "// button[contains(text(),'Import wallet')]"
            )
        )
        element_import_wallet.click()
        element_i_agree = wait.until(
            lambda d: d.find_element_by_xpath("// button[contains(text(),'I Agree')]")
        )
        element_i_agree.click()
        seed_input_amorce = wait.until(
            lambda d: d.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/div/div/form/div[4]/div[1]/div/input"
            )
        )
        seed_input_amorce.send_keys(
            "ice priority hard reason rely lift spray actual silk aware decide surprise"
        )
        mdp_input = wait.until(lambda d: d.find_element_by_xpath("//*[@id='password']"))
        mdp_input.send_keys("Kalimero2022")
        mdp_confirm_input = wait.until(
            lambda d: d.find_element_by_xpath("//*[@id='confirm-password']")
        )
        mdp_confirm_input.send_keys("Kalimero2022")
        tick_box = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div/div/form/div[7]/div"
        ).click()
        confirm_button = wait.until(
            lambda d: d.find_element_by_xpath("// button[contains(text(),'Import')]")
        )
        confirm_button.click()
        all_done_button = wait.until(
            lambda d: d.find_element_by_xpath("// button[contains(text(),'All Done')]")
        )
        all_done_button.click()
        POPUP_we_are_making = wait.until(
            lambda d: d.find_element_by_xpath(
                "/html/body/div[2]/div/div/section/header/div/button"
            )
        )
        POPUP_we_are_making.click()
        corner_button = wait.until(
            lambda d: d.find_element_by_xpath(
                "/html/body/div[1]/div/div[3]/div/div/div/div[1]/button"
            )
        )
        corner_button.click()
        account_details = wait.until(
            lambda d: d.find_element_by_xpath("/html/body/div[2]/div[2]/button[2]/span")
        )
        account_details.click()
        close_windows = wait.until(
            lambda d: d.find_element_by_xpath(
                "/html/body/div[1]/div/span/div[1]/div/div/div/button[1]"
            )
        )
        close_windows.click()
        parameters = driver.find_element_by_class_name("account-menu__icon")
        webdriver.ActionChains(driver).move_to_element(parameters).click(
            parameters
        ).perform()
        lock = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div[2]/button"
        )
        lock.click()
        selection_new_seed = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/div[3]/span/button"
        )
        selection_new_seed.click()

        global connexionBDD

        connexionBDD = sqlite3.connect(r"C:\Users\crypt\Desktop\MetaBot_vF\MetaBDD.db")
        curseur = connexionBDD.cursor()
        chercher_seed = curseur.execute(
            "SELECT * FROM MetaBDDTable WHERE statutSeed = 'VALIDE' AND adresseWallet IS NULL"
        )
        ajout_iteration = "UPDATE MetaBDDTable SET adresseWallet = ? WHERE seedId = ?"
        curseur_update = connexionBDD.cursor()

        for seed in chercher_seed:
            seed_testee = seed[1]
            seed_id_testee = seed[0]
            seed_input = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[3]/div/div/div/div[4]/div[1]/div/input"
            )
            seed_input.send_keys(seed_testee)
            mdp_input = wait.until(
                lambda d: d.find_element_by_xpath("//*[@id='password']")
            )
            mdp_input.send_keys("Kalimero2022")
            mdp_confirm_input = wait.until(
                lambda d: d.find_element_by_xpath("//*[@id='confirm-password']")
            )
            mdp_confirm_input.send_keys("Kalimero2022")
            restore_button = wait.until(
                lambda d: d.find_element_by_xpath(
                    "// button[contains(text(),'Restore')]"
                )
            )
            restore_button.click()
            bouton_menu = wait.until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[1]/div/div[3]/div/div/div/div[1]/button"
                )
            )
            bouton_menu.click()
            account_details = wait.until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[2]/div[2]/button[2]/span"
                )
            )
            account_details.click()
            Addresse = wait.until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[1]/div/span/div[1]/div/div/div/div[3]/div[2]/div/div/div[1]"
                ).get_attribute("innerHTML")
            )
            colonne_Adresse = (Addresse, seed_id_testee)
            curseur_update.execute(ajout_iteration, colonne_Adresse)
            connexionBDD.commit()
            print("Addresse enregistrée :", Addresse)
            close_windows = wait.until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[1]/div/span/div[1]/div/div/div/button[1]"
                )
            )
            close_windows.click()
            parameters = wait.until(
                lambda d: d.find_element_by_class_name("account-menu__icon")
            )
            webdriver.ActionChains(driver).move_to_element(parameters).click(
                parameters
            ).perform()
            lock = wait.until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[1]/div/div[3]/div[2]/button"
                )
            )
            lock.click()
            selection_new_seed = wait.until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[1]/div/div[3]/div/div/div[3]/span/button"
                )
            )
            selection_new_seed.click()
        connexionBDD.close()
        driver.quit()
        return 1
    except:
        connexionBDD.close()
        driver.quit()
        return 0

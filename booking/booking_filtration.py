# This file will include a class with instance methods.
# That will be responsible to interact with website
# After we have some results, to apply filtrations.
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver
    
    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 'div [data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        for star_value in star_values:
            for star_element in star_child_elements:
                if (str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars'):
                    star_element.click()

    def sort_criterion(self, criterion):
        sorter_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        sorter_button.click()
        criterion_button = self.driver.find_element(By.CSS_SELECTOR, f'button[data-id="{criterion}"]')
        criterion_button.click()
        # sorter_button_child_elements = sorter_button.find_element(By.CSS_SELECTOR, '*')

        # for sorter_button_child_element in sorter_button_child_elements:
        #     if(str(sorter_button_child_element.get_attribute('innerHTML').strip()) == f'{criterion}'):
        #         sorter_button_child_element.click()


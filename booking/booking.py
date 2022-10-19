import booking.constants as const
from selenium import webdriver
import os
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
# from selenium.webdriver.common.keys import Keys
from booking.booking_filtration import BookingFiltration
import time
from booking.booking_report import BookingReport
from prettytable import PrettyTable

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r";C:\Users\wngia\Documents\chromedriver_win32", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        super(Booking, self).__init__(options=options)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.implicitly_wait(15)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-tooltip-text="Choose your currency"]')
        currency_element.click()
        selected_currency_element = self.find_element(By.CSS_SELECTOR, f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        selected_currency_element.click()

    def select_place_to_go(self, destination):
        try:
            search_field = self.find_element(By.ID, 'ss')

        except:
            search_field = self.find_element(By.CSS_SELECTOR, 'input[placeholder="Where are you going?"]')
        
        search_field.clear()
        search_field.send_keys(destination)

        try:
            first_result = self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]')
        except:
            first_result = self.find_element()
        first_result.click()


    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in_date}"]')
        check_in_element.click()
        
        check_out_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out_date}"]')
        check_out_element.click()
    
    def select_adults(self, count=1): 
        selection_element = self.find_element(By.ID, 'xp__guests__toggle')
        selection_element.click()
        
        while True:
            decrease_adults_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
            decrease_adults_element.click()

            # If the value of adults reaches 1, we need to get out of the loop

            adults_value_element = self.find_element(By.ID, 'group_adults')
            adults_value = adults_value_element.get_attribute('value') # returns current adults count

            if int(adults_value) == 1:
                break
        
        increase_button_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')

        for i in range(count-1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(2, 4, 5)
        time.sleep(3) # allow time for star rating filtrations to finish loading before sorting
        
        # Apply sorting criterion
        # Distance from downtown or city centre: distance_from_search
        # Top picks for long stays: popularity
        # Homes & apartments first: upsort_bh
        # Price (lowest first): price
        # Best reviewed & lowest price: review_score_and_price
        # Stars (highest first): class
        # Stars (lowest first): class_asc
        # Star rating and price: class_and_price
        # Top reviewed: baysesian_review_score
        # Genius discounts first (available only if you had logged in): genius

        filtration.sort_criterion('distance_from_search')
    
    def report_results(self):
        hotel_boxes = self.find_element(By.ID, 'search_results_table')
        report = BookingReport(hotel_boxes)
        table = PrettyTable(field_names=['hotel_name', 'hotel_price', 'hotel_score', 'run_date'])
        table.add_rows(report.pull_deal_box_attributes())
        print(table)


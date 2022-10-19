# This file is going to include methods that will parse specific data that we need from each 'deal boxes'.

from datetime import datetime
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
import pandas as pd

class BookingReport():
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # Extracting hotel name
            hotel_name = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML').strip()
            hotel_price = deal_box.find_element(By.CSS_SELECTOR, 'span[class="fcab3ed991 bd73d13072"]').get_attribute('innerHTML').strip()
            hotel_price = ''.join(char for char in hotel_price if char.isnumeric())
            hotel_score = deal_box.find_element(By.CSS_SELECTOR, 'div[class="b5cd09854e d10a6220b4"]').get_attribute('innerHTML').strip()
            run_date = datetime.now().strftime("%Y-%m-%d")

            collection.append([hotel_name, hotel_price, hotel_score, run_date])

            
            df = pd.DataFrame(collection, columns=['hotel_name', 'hotel_price', 'hotel_score', 'run_date'])
            df.to_csv(f'booking_deal_{run_date}.csv', index=False)

        
        return collection

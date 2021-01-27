#!/usr/bin/env python
# coding: utf-8

# In[23]:


from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import pandas as pd

from time import sleep


# In[26]:


class eurojackpot_scrapper():
    
    
    def __init__(self):
        
        self.COLUMNS = ["Date", "Regular nums", "Supplementary nums"]
        self.FILENAME = "eurojackpot_draws.csv"
                
        # driver for browser must be in path, or specify its location by passing parameter "executable_path="
        self.browser = webdriver.Chrome()
        self.url = "https://www.eurojackpot.com/"
        self.numbers = pd.DataFrame(columns = self.COLUMNS)        
        self.browser.get(self.url)
        # wait for page to load
        wait_time = 8
        try:
            myElem = WebDriverWait(self.browser, wait_time).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/section[1]/div/div/div/div[1]/div/div/div/div/div[2]')))
            
        except TimeoutException:
            print(f"Sort checkbox has not loaded in {wait_time} seconds!")        
            
        self.year_select = 0
        self.date_select = 0

        
    def set_implicit_wait(self,n):        
        # setting implicit wait for webdriver
        self.browser.implicitly_wait(n)
        
        
    def set_sort_state(self, sort_state = True):        
        # aligns sort checkbox with the passed parameter, default on site is True,        
        sort_check_box_parent = self.browser.find_element_by_xpath(
            "/html/body/div[2]/main/section[1]/div/div/div/div[1]/div/div/div/div/div[2]")        
        
        if (sort_check_box_parent.get_attribute("class") == "sort sorted") != sort_state:
            actions = ActionChains(self.browser)
            actions.move_to_element(sort_check_box_parent)
            actions.click(sort_check_box_parent.find_element_by_tag_name("a")).perform()            
    
    
    def get_current_numbers(self):        
        # adds to pandas the row of data about the draw
        draw_date = self.date_select.first_selected_option.get_attribute("value")
        
        regular_numbers = self.browser.find_element_by_class_name("numbers_regular").text.split("\n")
        regular_numbers = list(map(int, regular_numbers))
        
        supl_numbers = self.browser.find_element_by_class_name("numbers_supplementary").text.split("\n")
        supl_numbers = list(map(int, supl_numbers))
        
        bot.numbers = bot.numbers.append({
            bot.COLUMNS[0]:draw_date, 
            bot.COLUMNS[1]:regular_numbers, 
            bot.COLUMNS[2]:supl_numbers}, 
            ignore_index = True)
    
    
    def select_next_draw(self):        
        # selects next draw via dropdown boxes of year and date
        self.year_select = Select(self.browser.find_element_by_class_name("yearDropdown"))
        # iterating over year options
        for year_opt_ndx in range(len(self.year_select.options)):            
            self.year_select.select_by_index(year_opt_ndx)            
            self.date_select = Select(self.browser.find_element_by_class_name("dateDropdown"))   
            # iterating over draw date options
            for date_opt_ndx in range(len(self.date_select.options)): 
                self.date_select.select_by_index(date_opt_ndx)                     
                yield(True)
        yield(False)
        
        
    def get_all_numbers(self, sort_state = True, wait_time = 3):
        # scrapes draws: dates and numbers; and saves to file
        if wait_time != 0:
            self.set_implicit_wait(wait_time)
            
        draws = self.select_next_draw()
        while next(draws):            
            self.set_sort_state(sort_state)
            sleep(wait_time)
            self.get_current_numbers()
            
        self.save_numbers_to_file()
        
        
    def save_numbers_to_file(self):
        
        self.numbers.to_csv(self.filename)
        
        


# In[25]:

if __name__ == "__main__":
    bot = eurojackpot_scrapper()
    bot.get_all_numbers(False, 3)


import os
import json
import datetime
import openpyxl
from pathlib import Path
from humanBehavior import *
from selenium import webdriver
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium.webdriver import ChromeOptions
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class LeopardSolutionsScraper:
    def __init__(self, creds, locations, sublocations, non_selected_cities, practice_area, keyword_search_string, keyword_type, keyword_find_with, firms, languages, honors, types, specialties, admits, status1, status2, min_salary, max_salary, exports):
        self.configs = LeopardSolutionsScraper.read_configs()
        self.user_name = self.configs["user_name"]
        self.password = self.configs["password"]
        self.creds = creds
        self.spreadsheet_id = self.configs["spreadsheet_id"]
        self.credentials = LeopardSolutionsScraper.get_googlesheet_credentials()
        self.url = "https://www.leopardsolutions.com/app/login"
        self.driver = LeopardSolutionsScraper.create_chrome_instance()
        self.exports = exports
        self.locations = locations
        self.sublocations = sublocations
        self.practice_area = practice_area
        self.keyword_search_string = keyword_search_string
        self.keyword_type = keyword_type
        self.keyword_find_with = keyword_find_with
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.firms = firms
        self.languages = languages
        self.honors = honors
        self.types = types
        self.specialties = specialties
        self.admits = admits
        self.status1 = status1
        self.status2 = status2
        self.non_selected_cities = non_selected_cities
        
    @staticmethod
    def read_configs():
        with open("./configs.json", "r") as file:
            configs = json.loads(file.read())
            return configs
            
    @staticmethod
    def get_googlesheet_credentials():
        credentials = None
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        service_account_file = './GoogleSheetKey.json'
        credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
        return credentials

    @staticmethod
    def create_chrome_instance():
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": "{}/Generated File/".format(os.getcwd()),
                 "directory_upgrade": True}
        chrome_options = ChromeOptions()
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=chrome_options)
        driver.maximize_window()
        return driver

    def login_to_website(self):
        self.driver.get(self.url)
        user_name_el = "//input[@placeholder='Email' or @name='UserName']"
        pasword_el = "//input[@placeholder='Password' or @name='Password']"
        submit_el = "//input[@value='Sign In' and @type='submit']"
        human_typer(self.driver, user_name_el, self.user_name)
        human_typer(self.driver, pasword_el, self.password)
        human_clicker_click(self.driver, submit_el)

    def search_jobs(self):
        button_to_search_link_el = "//a[contains(@href,'/app/jobs/search')]"
        button_for_editing_filters_el = "//a[text()='Search' and @data-target='#EditFilter']"
        submit_button_el = "//a[@id='btnSubmit']"
        locations_filter_el = "//span[text()='{}']/preceding-sibling::span/input"
        locations_filter_dropdown_el = "//span[text()='{}']/preceding-sibling::span/preceding-sibling::span"
        cities_filter_el = "//span[text()='{}']/preceding-sibling::span/input"
        practice_area_filter_el = "//span[text()='{}']/preceding-sibling::input"
        firms_filter_el = "//span[text()='{}']/preceding-sibling::input"
        languages_filter_el = "//span[text()='{}']/preceding-sibling::input"
        honors_filter_el = "//span[text()='{}']/preceding-sibling::input"
        specialties_filter_el = "//span[text()='{}']/preceding-sibling::input"
        admits_filter_el = "//span[text()='{}']/preceding-sibling::input"
        types_filter_el = "//span[text()='{}']/preceding-sibling::span/input"
        status1_filter_el = "//span[text()='{}']/parent::span/preceding-sibling::span/input"
        status2_filter_el = "//span[text()='{}']/preceding-sibling::input"
        keyword_search_el = "//input[@id='txtKeyword']"
        keyword_type_el = "//input[@value='{}']"
        keyword_find_with_el = "(//input[@value='{}'])[2]"
        min_salary_el = "//input[@id='txtMinSalary']"
        max_salary_el = "//input[@id='txtMaxSalary']"
        human_clicker_click(self.driver, button_to_search_link_el)
        human_clicker_click(self.driver, button_for_editing_filters_el)
        if self.locations:
            locations_el = "//a[@id='aFilterLocations']"
            human_clicker_click(self.driver,locations_el)
            for state in self.locations:
                try:
                    human_clicker_click(self.driver,locations_filter_el.format(state))
                except: ()
            random_wait(4,5)
            if self.sublocations:
                random_wait(2,3)
                try:
                    for country in self.sublocations:
                        move_to_element(self.driver,locations_filter_el.format(country))
                        human_clicker_click(self.driver,locations_filter_el.format(country))
                        human_clicker_click(self.driver,locations_filter_dropdown_el.format(country))
                except: ()
            if self.non_selected_cities:
                try:
                    for country in self.sublocations:
                        for unselect_city in self.non_selected_cities[country]:
                            move_to_element(self.driver,cities_filter_el.format(unselect_city))
                            human_clicker_click(self.driver,cities_filter_el.format(unselect_city))
                except: ()
        if self.practice_area:
            practice_area_el = "//a[@id='aFilterPracticeArea']"
            human_clicker_click(self.driver,practice_area_el)
            for item in self.practice_area:
                try:
                    human_clicker_click(self.driver,practice_area_filter_el.format(item))
                except: ()
        if self.keyword_search_string or self.keyword_type or self.keyword_find_with:
            keyword_el = "//a[@id='aFilterKeyword']"
            human_clicker_click(self.driver,keyword_el)
            if self.keyword_search_string:
                try:
                    human_typer(self.driver,keyword_search_el,self.keyword_search_string)
                except: ()
            if self.keyword_type:
                try:
                    human_clicker_click(self.driver,keyword_type_el.format(self.keyword_type))
                except: ()
            if self.keyword_find_with:
                try:
                    human_clicker_click(self.driver,keyword_find_with_el.format(self.keyword_find_with))
                except: ()
        if self.firms:
            firms_el = "//a[@id='aFilterFirms']"
            human_clicker_click(self.driver,firms_el)
            for item in self.firms:
                try:
                    move_to_element(self.driver,firms_filter_el.format(item))
                    human_clicker_click(self.driver,firms_filter_el.format(item))
                except: ()
        if self.languages:
            languages_el = "//a[@id='aFilterLanguages']"
            human_clicker_click(self.driver,languages_el)
            for item in self.languages:
                try:
                    human_clicker_click(self.driver,languages_filter_el.format(item))
                except: ()
        if self.honors:
            honors_el = "//a[@id='aFilterHonors']"
            human_clicker_click(self.driver,honors_el)
            for item in self.honors:
                try:
                    human_clicker_click(self.driver,honors_filter_el.format(item))
                except: ()
        if self.types:
            types_el = "//a[@id='aFilterTypes']"
            human_clicker_click(self.driver,types_el)
            random_wait(2,3)
            for item in self.types:
                try:
                    human_clicker_click(self.driver,types_filter_el.format(item))
                except: ()
        if self.specialties:
            specialties_el = "//a[@id='aFilterSpeacialties']"
            human_clicker_click(self.driver,specialties_el)
            for item in self.specialties:
                try:
                    move_to_element(self.driver,specialties_filter_el.format(item))
                    human_clicker_click(self.driver,specialties_filter_el.format(item))
                except: ()
        if self.admits:
            admits_el = "//a[@id='aFilterAdmits']"
            human_clicker_click(self.driver,admits_el)
            for item in self.admits:
                try:
                    move_to_element(self.driver,admits_filter_el.format(item))
                    human_clicker_click(self.driver,admits_filter_el.format(item))
                except: ()
        if self.status1 or self.status2:
            status_el = "//a[@id='aFilterStatus']"
            human_clicker_click(self.driver,status_el)
            if self.status1:
                for item in self.status1:
                    try:
                        human_clicker_click(self.driver,status1_filter_el.format(item))
                    except:()
            if self.status2:
                try:
                    human_clicker_click(self.driver,status2_filter_el.format(self.status2))
                except: ()
        if self.min_salary or self.max_salary:
            salary_el = "//a[@id='aFilterSalary']"
            human_clicker_click(self.driver,salary_el)
            if self.min_salary:
                try:
                    human_typer(self.driver,min_salary_el,self.min_salary)
                except: ()
            if self.max_salary:
                try:
                    human_typer(self.driver,max_salary_el,self.max_salary)
                except: ()
        random_wait(3,5)
        human_clicker_click(self.driver, submit_button_el)
        random_wait(4,6)
    
    def export_file(self):
        export_el = "//a[text()='Export']"
        export_what_el = "//select[@id='ddExportWhat']"
        all_results_el = "//option[@value='Results']"
        selected_results_el = "//option[@value='Selected']"
        submit_button_el = "//div[@id='Export']//a[text()='Submit']"
        if self.exports == ['Selected Results']:
            input("Hit enter after selecting the jobs.")
        else:
            self.exports = ["All Results"]
        human_clicker_click(self.driver,export_el)
        human_clicker_click(self.driver,export_what_el)
        if self.exports == ['All Results']:
            human_clicker_click(self.driver,all_results_el)
        if self.exports == ['Selected Results']:
            human_clicker_click(self.driver,selected_results_el)
        human_clicker_click(self.driver,submit_button_el)
        random_wait(20,40)
        self.driver.quit()
    
    def write_data_to_spreadsheet(self,_values):
        try:
            service = build('sheets', 'v4', credentials=self.credentials)
            body = {
                'values': _values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId= self.spreadsheet_id, range="Sheet1!A1",
                valueInputOption="USER_ENTERED", body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
            
    @staticmethod
    def check_token_expiration():
        creds = None
        SCOPES = ['https://www.googleapis.com/auth/drive']
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'DriveCredentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    
    def upload_file_to_drive(self,file_name):
        service = build('drive', 'v3', credentials=self.creds)
        file_metadata = {'name' : file_name + '.txt'}
        media = MediaFileUpload('./Generated File/' + file_name + '.txt',mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media,fields='id').execute()
        
    def read_data_from_xlsx(self):
        file_path = None
        data_format = """{} - {}\n{}\n\n\n\n\n\n"""
        file_data = ""
        for root,dir_path,files in os.walk("Generated File"):
            for file in files:
                if '.xlsx' in file:
                    file_path = Path("Generated File",file)
        wb_obj = openpyxl.load_workbook(file_path)
        ws = wb_obj.active
        data = ws.values
        data_list = []
        initial = True
        for item in data:
            if initial:
                # data_list.append([item[1],item[2],item[6],item[9]])
                initial = False
                pass
            else:
                data_list.append([item[1],item[2],item[6],item[9].split(" ")[0]])
        first_index_data = data_list.pop(0)
        data_list.sort(key=lambda date: datetime.datetime.strptime(date[-1],'%m/%d/%Y'),reverse=True)
        data_list.insert(0,first_index_data)
        for item in data_list:
            file_data += data_format.format(item[0],item[1],item[2])
        file_name = datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S")
        with open('./Generated File/' + file_name + '.txt', 'w') as f:
            f.write(file_data)
        # self.write_data_to_spreadsheet(data_list)
        os.remove(file_path)
        self.upload_file_to_drive(file_name)
        print("uploading finished")
        os.remove('./Generated File/' + file_name + '.txt')



def main(creds, locations, sublocations, non_selected_cities, practice_area, keyword_search_string, keyword_type, keyword_find_with, firms, languages, honors, types, specialties, admits, status1, status2, min_salary, max_salary, exports):
    leopard_solutions_scraper = LeopardSolutionsScraper(creds, locations, sublocations, non_selected_cities, practice_area, keyword_search_string, keyword_type, keyword_find_with, firms, languages, honors, types, specialties, admits, status1, status2, min_salary, max_salary, exports)
    leopard_solutions_scraper.login_to_website()
    leopard_solutions_scraper.search_jobs()
    leopard_solutions_scraper.export_file()
    leopard_solutions_scraper.read_data_from_xlsx()
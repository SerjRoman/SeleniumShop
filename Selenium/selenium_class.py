
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException,ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumBase:
    def __init__(self):
        self.SERVICE = None
        self.OPTIONS = None
        self.DRIVER = None

    def create_chrome_service(self):
        service = Service(ChromeDriverManager().install())
        self.SERVICE = service
    
    def create_options(self):
        options = Options()
        self.OPTIONS = options
    
    def create_chrome_driver(self):
        if self.OPTIONS == None:
            raise RuntimeError('Options is not created, Error: 0')
        if self.SERVICE == None:
            raise RuntimeError('Service is not created, Error: 1')
        if not type(self.SERVICE) is Service:
            raise RuntimeError('Service created improperly, Error: 2')
        if not type(self.OPTIONS) is Options:
            raise RuntimeError('Options created improperly, Error: 3')
        
        driver = webdriver.Chrome(service=self.SERVICE, options=self.OPTIONS)
        self.DRIVER = driver
    def add_options_argument(self, argument):
        
        if self.OPTIONS == None:
            raise RuntimeError('Options is not created, Error: 0')
        
        if type(argument) is str:
            self.__add_options_argument(argument=argument)

    def add_options_arguments(self, arguments):
        
        if self.OPTIONS == None:
            raise RuntimeError('Options is not created, Error: 0')
        
        if type(arguments) is list:
            for argument in arguments:
                if type(argument) is str:
                    self.__add_options_argument(argument=argument)

    def __add_options_argument(self, argument):
        self.OPTIONS.add_argument(argument)

class Driver(SeleniumBase):
    def __init__(self) -> None:
        super().__init__()
        self.TIMEOUT = 5
    
    def _check_driver_existence(self):
        if self.DRIVER == None:
            raise RuntimeError('Driver was NOT created')
        if not type(self.DRIVER) is webdriver.Chrome:
            raise RuntimeError('Driver was created improperly')

    def go_to(self, url):
        self._check_driver_existence()

        if not type(url) is str:
            raise RuntimeError('Improper type of URL')
        if not 'https://' in url or not 'http://' in url:
            raise RuntimeError('Improper URL')
        try:
            self.DRIVER.get(url=url)
        except Exception as error:
            raise RuntimeError(f'${error}')
        self.wait_page_loaded()
        self.scroll_page_to_bottom()
    def find_element_by_xpath(self, xpath, click=False ):
        self._check_driver_existence()

        if xpath == None:
            raise ValueError('Xpath is None')
        try:
            self.wait_element_present(xpath=xpath)
            if click:
                self.wait_element_clickable(xpath)
                
            element = self.DRIVER.find_element(by = By.XPATH, value=xpath)
            if click:
                self.DRIVER.execute_script("arguments[0].click()", element)
            # if not element.is_displayed():
            #     raise ElementNotVisibleException('Element is not visible')
            return element
        except ElementNotVisibleException:
            raise ElementNotVisibleException('Element is not visible')
        except NoSuchElementException:
            raise NoSuchElementException('Element is not found')
        except ElementClickInterceptedException:
            raise ElementClickInterceptedException('Element is not clickable')
        except Exception as error:
            raise RuntimeError(f'${error}')
        
    def find_elements_by_xpath(self, xpath ):
        self._check_driver_existence()

        if xpath == None:
            raise ValueError('Xpath is None')
        try:
            self.wait_element_present(xpath=xpath)
                
            elements = self.DRIVER.find_element(by = By.XPATH, value=xpath)
            # if not element.is_displayed():
            #     raise ElementNotVisibleException('Element is not visible')
            return elements
        except ElementNotVisibleException:
            raise ElementNotVisibleException('Element is not visible')
        except NoSuchElementException:
            raise NoSuchElementException('Element is not found')
        except ElementClickInterceptedException:
            raise ElementClickInterceptedException('Element is not clickable')
        except Exception as error:
            raise RuntimeError(f'${error}')
        

    def wait_element_visibile(self, xpath) -> bool:
        try:
            element_present = EC.visibility_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.DRIVER, self.TIMEOUT).until(element_present) 
        except TimeoutException:
            raise TimeoutException('Timed out waiting for element to load')
        except Exception as error:
            raise RuntimeError(f'${error}')
    def wait_element_present(self, xpath):
        try:
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.DRIVER, self.TIMEOUT).until(element_present) 
        except TimeoutException:
            raise TimeoutException('Timed out waiting for element to load')
        except Exception as error:
            raise RuntimeError(f'${error}')
        
    def wait_element_clickable(self, xpath):
        try:
            element_present = EC.element_to_be_clickable((By.XPATH, xpath))
            WebDriverWait(self.DRIVER, self.TIMEOUT).until(element_present) 
        except TimeoutException:
            raise TimeoutException('Timed out waiting for element to load')
        except Exception as error:
            raise RuntimeError(f'${error}')
        
    def wait_page_loaded(self):
        WebDriverWait(self.DRIVER, self.TIMEOUT).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    def scroll_page_to_bottom(self):
        self.DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def get_attribute(self, element, attribute):
        attribute_data = element.get_attribute(attribute)
        if attribute_data is None:
            raise ValueError('No such attribute/No attribute data')
        
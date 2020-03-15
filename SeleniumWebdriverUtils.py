'''
Created on 31 ene. 2020

@author: aoviedo

This is a module that offers some methods to perform some tasks and are complex or tedious to code
but are useful or have to be performed frequently.
'''
__version__= "0.1.0"
import time
import os
import datetime
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#This is a global parameter used to name our screenshots when we are using the method 
#getFullScreenshotScrollinggetFullScreenshotScrolling
partialImage = 0
#This is a global parameter used to set the timeout when looking for an HTML element
timeout = 10

def getDocumentHeight(driver):
    '''
    This method executes several JavaScript scripts to get the height of the HTML document
    (as a whole), not the window size

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts

    Returns
    -------
    int
        The height of the HTML document
    '''
    #In this list we will we adding all the different heights that our different JavaScript scripts
    #will be returning
    v = []
    #Here we will save all the capabilities that were set in our driver so we can get the browser name
    caps = driver.capabilities
    #Now, we will execute all the different JavaScript scripts and add their results to our list
    #Notice, we will filter where we apply our scripts depending on the browser (not all browsers
    #are the same and support the same JavaScript functions)
    if(caps['browserName'] != "Safari"):
        v.append(driver.execute_script("return document.body.scrollHeight"))
    v.append(driver.execute_script("return document.documentElement.scrollHeight"))
    v.append(driver.execute_script("return document.body.offsetHeight"))
    if(caps['browserName'] != "Safari" and ("platformName" not in caps.keys() or caps["platformName"] == "Android")):
        v.append(driver.execute_script("return document.documentElement.offsetHeight"))
    v.append(driver.execute_script("return document.body.clientHeight"))
    v.append(driver.execute_script("return document.documentElement.clientHeight"))
    
    #In this list we will add all the "real" heights that our scripts returned, all the ones
    #that were different than None    
    heights = []
    for vv in v:
        if vv is not None:
            heights.append(vv)
    #We will return the greater height
    return max(heights)

def getDocumentWidth(driver):
    '''
    This method executes several JavaScript scripts to get the height of the HTML document
    (as a whole), not the window size

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts

    Returns
    -------
    int
        The height of the HTML document
    '''
    #In this list we will we adding all the different widths that our different JavaScript scripts
    #will be returning
    v = []
    #Here we will save all the capabilities that were set in our driver so we can get the browser name
    caps = driver.capabilities
    #Now, we will execute all the different JavaScript scripts and add their results to our list
    #Notice, we will filter where we apply our scripts depending on the browser (not all browsers
    #are the same and support the same JavaScript functions)
    if(caps['browserName'] != "Safari"):
        v.append(driver.execute_script("return document.body.scrollWidth"))
    v.append(driver.execute_script("return document.documentElement.scrollWidth"))
    v.append(driver.execute_script("return document.body.offsetWidth"))
    if(caps['browserName'] != "Safari" and ("platformName" not in caps.keys() or caps["platformName"] == "Android")):
        v.append(driver.execute_script("return document.documentElement.offsetWidth"))
    v.append(driver.execute_script("return document.body.clientWidth"))
    v.append(driver.execute_script("return document.documentElement.clientWidth"))
    #In this list we will add all the "real" widths that our scripts returned, all the ones
    #that were different than None 
    widths = []
    for vv in v:
        if vv is not None:
            widths.append(vv)
    #We will return the greatest width
    return max(widths)

def getInnerWindowHeight(driver):
    '''
    This method executes a JavaScript script to get the height of the inner part of the window

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts

    Returns
    -------
    int
        The height of inner part of the window
    '''
    return driver.execute_script("return window.innerHeight")
     
def getInnerWindowWidth(driver):
    '''
    This method executes a JavaScript script to get the width of the inner part of the window

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts

    Returns
    -------
    int
        The width of inner part of the window
    '''
    return driver.execute_script("return window.innerWidth")  

        
def goToTopPage(driver):
    '''
    This method executes a JavaScript script to scroll to the top of the HTML document

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts

    Returns
    -------
    None
    '''
    #First we get the height of the HTML document
    docHeight = getDocumentHeight(driver)
    #We create a script in JavaScript that scroll to the top
    toTopPage = "window.scrollBy(0,-{0})".format(docHeight+100)
    #We execute that script
    driver.execute_script(toTopPage)

def hideScrollBar(driver):
    '''
    This method executes a JavaScript script that hides the scroll bar

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts

    Returns
    -------
    None
    '''
    driver.execute_script("document.body.style.overflow = 'hidden';")
  
def scrollWindow(driver,func=None,*parameters):
    '''
    This method executes a JavaScript script that scroll our page from top to bottom

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    func: Python function
        This allows the possibility to execute a function during each iteration of this scrolling
        function. For instance, take screenshots
    parameters:
        This will contain all the necessary parameters to execute the function in the parameter
        "func"

    Returns
    -------
    None
    '''
    #We get the HTML document height
    docHeight = getDocumentHeight(driver)
    print("height: {0}".format(docHeight))
    #We scroll to the top of the page
    goToTopPage(driver)
    #x represents our position in the page
    x = 0
    #While x is not greater than the height of the document, it means we can keep scrolling
    while(x<docHeight):
        #We hide the scroll bar
        hideScrollBar(driver)
        #We sleep for 2 seconds to allow the former change to have effect
        time.sleep(2)
        #We try to execute the function "func" that we passed as parameter using the
        #parameters in the list *parameters
        try:
            func(*parameters)
        except Exception as e:
            #If the function returns a Exception, we catch it
            print("An exception ocurred while we were executing the function passed as parameter: {0}".format(e))
        #We get the inner size of our current wndow, we add it to our current position in variable
        #x (minus 100 pixels)
        x = x + (getInnerWindowHeight(driver)-100)
        #We code a JavaScript script to scroll to that point
        scrollIt = "window.scrollTo(0,{0})".format(x)
        print("Position: {0}".format(x))
        #We execute that script to scroll to that point
        driver.execute_script(scrollIt)
        

def getPartialScrollImage(driver,imageTitle):
    '''
    This method names our partial screenshots that we get while scrolling the page from top to bottom

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    imageTitle: string
        Root of the name for this screenshot
    Returns
    -------
    None
    '''
    #We get the global variable partialImage
    global partialImage
    #We save this screenshot, using partialImage as the last part of the name for this screenshot
    driver.get_screenshot_as_file(imageTitle+"-{0}".format(partialImage)+".jpg")
    #We increase the counter partialImage by 1
    partialImage+=1

def getFullScreenshotScrolling(driver,imageTitle,folder=None):
    '''
    This method gets screenshots of our current page, scrolling from top to bottom and getting
    a screenshot in each iteration, using the method scrollWindow described above

    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    imageTitle: string
        Root of the name for this screenshot
    folder: string
        path to the folder where we want to save our screenshots
        if none, we will create one using the current date and time
    Returns
    -------
    None
    '''
    #If folder is None, we provide a name for the folder that will contain our screenshots
    #using the current date and time as a basis
    if(folder is None):
        folder= "{0}".format(datetime.datetime.today()).replace(":","-")
    #We create the folder that will contain our screenshots
    os.mkdir(folder)
    #We set the complete that for our image combining the variable path and imageTitle
    imagePath = folder+"/"+imageTitle
    #We call to the method scrollWindow using getPartilScrollImage as the function func
    #and driver and imagePath as part of the variables in the variables list *parameters
    scrollWindow(driver, getPartialScrollImage,driver,imagePath)
    #We get the global variable partialImage
    global partialImage
    #And set it to 0 as we have finished the process so it has to point to 0 again
    partialImage = 0
    
def getFullScreenshotHeadless(driver,imageTitle,webdriverpath=None):
    '''
    This method opens a headless browser using webdriverpath (in case is not Noe), 
    goes to the URL in the parameter driver and copies the cookies (to assure we see the same in
    case we are logged in)
    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    imageTitle: string
        Name for the file that will contain our screenshot
    webdriverpath: string
        Path to the webdriver for our headless browser
    Returns
    -------
    None
    '''
    #We check if our driver is a Chrome or a Firefox driver
    #And create the corresponding headless webdriver using the parameter
    #webdriverpath in caxe it was provided, if it was not we are assuming webdrivers
    #paths have been added to the environment variable PATH, otherwise it won't work
    if isinstance(driver,webdriver.Chrome):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        options.add_argument('headless')
        if webdriverpath is not None:
            driverHeadless = webdriver.Chrome(executable_path=webdriverpath,chrome_options=options)
        else:
            driverHeadless = webdriver.Chrome(chrome_options=options)
    elif isinstance(driver, webdriver.Firefox):
        options = Options()
        options.headless = True
        if webdriverpath is not None:
            driver = webdriver.Firefox(executable_path=webdriverpath,options=options)
        else:
            driver = webdriver.Firefox(options=options)
    else:
        #If it was not Chrome or Firefox, we raise an Exception as the other webdrivers
        #don't support headless capabilities
        raise Exception("Browser Not Supported")
    #We go to the url where we where in our driver    
    driverHeadless.get(driver.current_url)
    #We copy the cookies from our original driver to our headless driver
    for cookie in driver.get_cookies():
        if 'expiry' in cookie.keys():
            del cookie['expiry']
        driverHeadless.add_cookie(cookie)
    #We get the height of the whole HTML document
    docHeight = getDocumentHeight(driver)
    #We get the width of the whole HTML document
    docWidth = getDocumentWidth(driver)
    #We resize our headless browser to the size of the whole HTML document
    driverHeadless.set_window_size(docWidth+3000, docHeight)
    #We get a screenshot
    driverHeadless.get_screenshot_as_file("{0}.jpg".format(imageTitle))
    #We close our headless driver
    driverHeadless.quit()
    
def find_element_implicitwait(driver,by,selector):
    '''
    This method finds an element like the actual method offered by selenium.webdriver but
    it waits until the element is present in the DOM (although there is a timeout after
    which it will fail and raise an exception)
    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    by: selenium.webdriver.common.by
        Way in which we will search for our element, By.ID, By.XPATH, By.CLASS_NAME
    selector: string
        Selector that we will use, the ID of the element if we are using By.ID, the xpath if
        we are using By.XPATH...
    Returns
    -------
    webdriver HTML element
    '''
    #We get the timeout get set for this search
    global timeout
    #We search for the element
    elem = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by,selector))
        )
    #We return the element
    return elem

def find_element_by_id_implicitwait(driver,vId):
    '''
    This method finds an element by ID like the actual method offered by selenium.webdriver but
    it waits until the element is present in the DOM (although there is a timeout after
    which it will fail and raise an exception) using the method find_element_implicitwait
    described above
    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    id: string
        ID of the HTML element
    Returns
    -------
    webdriver HTML element
    '''    
    return find_element_implicitwait(driver, By.ID, vId)

def find_element_by_xpath_implicitwait(driver,xpath):
    '''
    This method finds an element by XPATH like the actual method offered by selenium.webdriver but
    it waits until the element is present in the DOM (although there is a timeout after
    which it will fail and raise an exception) using the method find_element_implicitwait
    described above
    Parameters
    ----------
    driver : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    xpath: string
        XPATH of the HTML element
    Returns
    -------
    webdriver HTML element
    '''      
    return find_element_implicitwait(driver, By.XPATH, xpath)

def set_implicit_wait_timeout(newTimeout):
    '''
    This method, sets the timeout for the implicit wait in method find_element_implicitwait
    and the ones that extend it
    Parameters
    ----------
    newTimeout : selenium.webdriver
        This is the driver controlling the browser where we will execute the JavaScript scripts
    Returns
    -------
    None
    '''
    global timeout
    timeout = newTimeout
    
def capabilities_remove_automation_bar_Chrome():
    '''
    This method returns an object of type ChromeOptions that contains the capabilities necessary
    to remove the bar that states that the browser is being controlled by an automation machine
    in Chrome. You have have to give the parameter options in the constructor the value of the
    return of this method
    Parameters
    ----------
    None
   
    Returns
    -------
    chrome_options webdriver.ChromeOptions object
    '''
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
    chrome_options.add_experimental_option("useAutomationExtension", False);
    chrome_options.add_experimental_option("prefs", {
        'credentials_enable_service:':False,
        'profile': {
            'password_manager_enabled':False
            }
        })
    return chrome_options 
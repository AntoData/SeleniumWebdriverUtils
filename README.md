# SeleniumWebdriverUtils
 Module that offers additional and useful methods for Selenium's Webdriver

Methods offered:
- getDocumentHeight:
  This method executes several JavaScript scripts to get the height of the HTML document (as a whole), not the window size
    
- getDocumentWidth:
  This method executes several JavaScript scripts to get the height of the HTML document (as a whole), not the window size
  
- getInnerWindowHeight:
  This method executes a JavaScript script to get the height of the inner part of the window

- getInnerWindowWidth:
  This method executes a JavaScript script to get the width of the inner part of the window
        
- goToTopPage:
  This method executes a JavaScript script to scroll to the top of the HTML document

- hideScrollBar:
  This method executes a JavaScript script that hides the scroll bar

- scrollWindow:
  This method executes a JavaScript script that scroll our page from top to bottom

- getPartialScrollImage:
  This method names our partial screenshots that we get while scrolling the page from top to bottom

- getFullScreenshotScrolling:
  This method gets screenshots of our current page, scrolling from top to bottom and getting a screenshot in each iteration, using the method scrollWindow described above
    
- getFullScreenshotHeadless:
  This method opens a headless browser using webdriverpath (in case is not Noe), goes to the URL in the parameter driver and copies the cookies (to assure we see the same in case we are logged in)
    
- find_element_implicitwait:
  This method finds an element like the actual method offered by selenium.webdriver but it waits until the element is present in the DOM (although there is a timeout after which it will fail and raise an exception)
  
- find_element_by_id_implicitwait:
  This method finds an element by ID like the actual method offered by selenium.webdriver but it waits until the element is present in the DOM (although there is a timeout after which it will fail and raise an exception) using the method find_element_implicitwait described above
  
- find_element_by_xpath_implicitwait:
  This method finds an element by XPATH like the actual method offered by selenium.webdriver but it waits until the element is present in the DOM (although there is a timeout after which it will fail and raise an exception) using the method find_element_implicitwait described above

- set_implicit_wait_timeout:
  This method, sets the timeout for the implicit wait in method find_element_implicitwait and the ones that extend it

- capabilities_remove_automation_bar_Chrome:
  This method returns an object of type ChromeOptions that contains the capabilities necessary to remove the bar that states that the browser is being controlled by an automation machine in Chrome. You have have to give the parameter options in the constructor the value of the return of this method

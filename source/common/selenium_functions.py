import logging
import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver as wiredriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import source.common.connections_functions as conn_func

REPOSITORY_PATH = Path(__file__).parent.parent.parent


def initialize_webdriver(webdriver_type=None, headless=False, download_path=None, profile=None,
                         undetectable=False, allow_download_images=True, random_useragent=False,
                         custom_useragent=''):
    """
    Function that is responsible for browser initialization.
    :param webdriver_type: Choose between Chrome and Firefox.
    :param headless: If will be headless or not.
    :param download_path: custom path for downloads.
    :param profile: firefox profile path.
    :param undetectable: if browser is undetectable for cloudflare anti-bot system.
    :param allow_download_images: allow image loading.
    :param random_useragent: use random useragent or not.
    :param custom_useragent: if you use a custom useragent.
    :return:
    """
    global browser
    # Creates a working directory, to download things etc.
    if download_path is None:
        download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory")
        if not os.path.exists(os.path.dirname(download_path)):
            os.mkdir(os.path.dirname(download_path))

        download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory/test.txt")
        if not os.path.exists(os.path.dirname(download_path)):
            os.mkdir(os.path.dirname(download_path))

        download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory/downloads/test.txt")
        if not os.path.exists(os.path.dirname(download_path)):
            os.mkdir(os.path.dirname(download_path))

        download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory/downloads")

    chrome_executable_path = ChromeDriverManager().install()
    gecko_executable_path = GeckoDriverManager().install()

    if undetectable:
        if webdriver_type == 'firefox':
            print('not configured')
        elif 'chrome' in webdriver_type:
            print('Initializing Chrome')
            options = webdriver.ChromeOptions()

            options.headless = False
            options.add_argument("--window-size=1920,1080")

            if allow_download_images:
                pass
            else:
                # PREFS TO DOESNT DOWNLOAD IMAGES AND DISK CACHE SIZE removed: , 'disk-cache-size': 4096
                prefs = {"profile.managed_default_content_settings.images": 2}
                options.add_experimental_option("prefs", prefs)

            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument(str('user-agent=' + conn_func.get_useragent()))
            browser = wiredriver.Chrome(executable_path=chrome_executable_path, options=options)
            browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                "source": '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                            get: function() { return {"0":{"0":{}},"1":{"0":{}},"2":{"0":{},"1":{}}}; }
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ["en-US", "en"]
                    });
                    Object.defineProperty(navigator, 'mimeTypes', {
                        get: function() { return {"0":{},"1":{},"2":{},"3":{}}; }
                    });

                    window.screenY=23;
                    window.screenTop=23;
                    window.outerWidth=1337;
                    window.outerHeight=825;
                    window.chrome =
                    {
                      app: {
                        isInstalled: false,
                      },
                      webstore: {
                        onInstallStageChanged: {},
                        onDownloadProgress: {},
                      },
                      runtime: {
                        PlatformOs: {
                          MAC: 'mac',
                          WIN: 'win',
                          ANDROID: 'android',
                          CROS: 'cros',
                          LINUX: 'linux',
                          OPENBSD: 'openbsd',
                        },
                        PlatformArch: {
                          ARM: 'arm',
                          X86_32: 'x86-32',
                          X86_64: 'x86-64',
                        },
                        PlatformNaclArch: {
                          ARM: 'arm',
                          X86_32: 'x86-32',
                          X86_64: 'x86-64',
                        },
                        RequestUpdateCheckStatus: {
                          THROTTLED: 'throttled',
                          NO_UPDATE: 'no_update',
                          UPDATE_AVAILABLE: 'update_available',
                        },
                        OnInstalledReason: {
                          INSTALL: 'install',
                          UPDATE: 'update',
                          CHROME_UPDATE: 'chrome_update',
                          SHARED_MODULE_UPDATE: 'shared_module_update',
                        },
                        OnRestartRequiredReason: {
                          APP_UPDATE: 'app_update',
                          OS_UPDATE: 'os_update',
                          PERIODIC: 'periodic',
                        },
                      },
                    };
                    window.navigator.chrome =
                    {
                      app: {
                        isInstalled: false,
                      },
                      webstore: {
                        onInstallStageChanged: {},
                        onDownloadProgress: {},
                      },
                      runtime: {
                        PlatformOs: {
                          MAC: 'mac',
                          WIN: 'win',
                          ANDROID: 'android',
                          CROS: 'cros',
                          LINUX: 'linux',
                          OPENBSD: 'openbsd',
                        },
                        PlatformArch: {
                          ARM: 'arm',
                          X86_32: 'x86-32',
                          X86_64: 'x86-64',
                        },
                        PlatformNaclArch: {
                          ARM: 'arm',
                          X86_32: 'x86-32',
                          X86_64: 'x86-64',
                        },
                        RequestUpdateCheckStatus: {
                          THROTTLED: 'throttled',
                          NO_UPDATE: 'no_update',
                          UPDATE_AVAILABLE: 'update_available',
                        },
                        OnInstalledReason: {
                          INSTALL: 'install',
                          UPDATE: 'update',
                          CHROME_UPDATE: 'chrome_update',
                          SHARED_MODULE_UPDATE: 'shared_module_update',
                        },
                        OnRestartRequiredReason: {
                          APP_UPDATE: 'app_update',
                          OS_UPDATE: 'os_update',
                          PERIODIC: 'periodic',
                        },
                      },
                    };
                    ['height', 'width'].forEach(property => {
                        const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);

                        // redefine the property with a patched descriptor
                        Object.defineProperty(HTMLImageElement.prototype, property, {
                            ...imageDescriptor,
                            get: function() {
                                // return an arbitrary non-zero dimension if the image failed to load
                            if (this.complete && this.naturalHeight == 0) {
                                return 20;
                            }
                                return imageDescriptor.get.apply(this);
                            },
                        });
                    });

                    const getParameter = WebGLRenderingContext.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function(parameter) {
                        if (parameter === 37445) {
                            return 'Intel Open Source Technology Center';
                        }
                        if (parameter === 37446) {
                            return 'Mesa DRI Intel(R) Ivybridge Mobile ';
                        }

                        return getParameter(parameter);
                    };

                    const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');

                    Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
                        ...elementDescriptor,
                        get: function() {
                            if (this.id === 'modernizr') {
                            return 1;
                            }
                            return elementDescriptor.get.apply(this);
                        },
                    });
                    '''
            })

    else:
        if webdriver_type == 'firefox':
            # Webdriver configurations
            start = time.time()
            print('Initializing Firefox Webdriver')
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True
            options = Options()
            options.headless = headless

            options.set_preference("browser.download.folderList", 2)  # tells it not to use default Downloads directory
            options.set_preference("browser.download.manager.showWhenStarting",
                                   False)  # turns of showing download progress
            options.set_preference("browser.helperApps.alwaysAsk.force", False)
            options.set_preference("browser.download.dir", str(download_path))  # sets the directory for downloads
            options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                   "text/plain, application/octet-stream, application/binary, text/csv, application/csv,"
                                   " application/excel, text/comma-separated-values, text/xml, application/xml,	"
                                   "image/svg+xml, image/svg,image/SVG, image/png,image/x-citrix-png,image/x-png ")  # tells Firefox to automatically download the files of the selected mime-types

            if profile is None:
                browser = webdriver.Firefox(executable_path=gecko_executable_path, options=options,
                                            capabilities=firefox_capabilities)  # starts driver
            else:
                userAgent = conn_func.get_useragent()
                print(userAgent)
                profile = webdriver.FirefoxProfile(profile)
                profile.set_preference("general.useragent.override", userAgent)
                profile.set_preference("dom.webdriver.enabled", False)
                profile.set_preference('useAutomationExtension', False)
                profile.update_preferences()
                desired = DesiredCapabilities.FIREFOX

                browser = webdriver.Firefox(executable_path=gecko_executable_path, options=options,
                                            capabilities=firefox_capabilities, firefox_profile=profile,
                                            desired_capabilities=desired)  # starts driver
                browser.maximize_window()
        elif 'chrome' in webdriver_type:
            print('Initializing Chrome')
            options = webdriver.ChromeOptions()
            # If options.headless = True, the website will not load
            options.headless = False
            options.add_argument("--window-size=1920,1080")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-blink-features=AutomationControlled')
            if random_useragent:
                current_useragent = conn_func.get_useragent()
                print(current_useragent)
                options.add_argument(str('user-agent=' + current_useragent))
            if custom_useragent != '':
                print('Using custom useragent: ', custom_useragent)
                options.add_argument(str('user-agent=' + custom_useragent))

            prefs = {'download.default_directory': str(download_path)}
            options.add_experimental_option('prefs', prefs)
            browser = webdriver.Chrome(executable_path=chrome_executable_path, options=options)

    return browser


""" Element Handlers to webdriver """


def wait_element_appear(MAXTIME, XPATH, browser):
    """
    Function that wait some element appear.
    :param MAXTIME: Limit of time to wait element
    :param XPATH: xpath of element
    :param browser: browser
    :return:
    """
    LOADING_ELEMENT_XPATH = XPATH
    try:
        WebDriverWait(browser, MAXTIME
                      ).until(EC.presence_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
        logging.debug("Waited element appear")
        return True
    except TimeoutException:
        logging.debug("Doesn't Wait element appear")
        return False


def wait_element_disappear(MAXTIME, XPATH, browser):
    """
        Function that wait some element disappear.
        :param MAXTIME: Limit of time to wait element
        :param XPATH: xpath of element
        :param browser: browser
        :return:
        """
    LOADING_ELEMENT_XPATH = XPATH
    try:
        WebDriverWait(browser, MAXTIME
                      ).until_not(EC.presence_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
        logging.debug("Waited element disappear")
    except TimeoutException:
        logging.debug("Doesn't Wait element disappear")


def wait_loading(MAXTIME, XPATH, browser):
    """
        Function that wait some element load.
        :param MAXTIME: Limit of time to wait element
        :param XPATH: xpath of element
        :param browser: browser
        :return:
        """
    try:
        WebDriverWait(browser, MAXTIME
                      ).until(EC.presence_of_element_located((By.XPATH, XPATH)))
        logging.debug("Loading waited")
    except TimeoutException:
        logging.debug("Loading appeared")

    try:
        WebDriverWait(browser, MAXTIME
                      ).until_not(EC.presence_of_element_located((By.XPATH, XPATH)))
        logging.debug("Waited loading disappear")
    except TimeoutException:
        logging.debug("Loading fail")


def scroll_down(browser, times=1, scroll_seconds=1, bottom=False):
    """
    This function makes scroll down webpage.
    :param browser:
    :param times:
    :param scroll_seconds:
    :param bottom:
    :return:
    """
    for i in range(times):
        if bottom:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            body = browser.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_DOWN)
        time.sleep(scroll_seconds)


def scroll_down_infinite(browser, scroll_time=1, bottom=False):
    """
    Scroll down infinite. Nice usage on social medias.
    :param browser:
    :param scroll_time:
    :param bottom:
    :return:
    """
    SCROLL_PAUSE_TIME = scroll_time

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        if bottom:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            body = browser.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_DOWN)
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def save_html(browser):
    """
    Saves HTML PAGE
    :param browser:
    :return:
    """
    with open('page.html', 'w') as f:
        f.write(browser.page_source)

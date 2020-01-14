import pytesseract as pytesseract
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from twython import Twython, TwythonError
# With the Selenium API
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import time
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter


"""
Classe permettant d'effectuer des actions sur Twitter, avec le navigateur Firefox en arrière plan
"""


class Twitter_API:
    """
    Navigateur qui va effecter les actions (on utilise Firefox), vide si inutilisé
    """
    driver = ""

    """
    Page d'accueil du compte (pour uniformiser la deconnexion)
    :type : string
    """
    main_page = "https://twitter.com/home"

    APP_KEY = 'à demander'
    APP_SECRET = 'à demander'

    def logIn2(self, token1, token2):
        """
        Fonction permettant de se connecter
        :param token1: nom de compte
        :param token2:  mot de passe du compte
        :return:
        :type token1: String
        :type token2: String
        :rtype: void
        """
        self.driver = webdriver.Firefox()
        self.driver.get("https://twitter.com/login")

        username_field = self.driver.find_element_by_class_name("js-username-field")
        password_field = self.driver.find_element_by_class_name("js-password-field")

        time.sleep(2)
        username_field.send_keys(token1)
        self.driver.implicitly_wait(1)

        time.sleep(2)
        password_field.send_keys(token2)
        self.driver.implicitly_wait(1)

        self.driver.find_element_by_class_name("EdgeButtom--medium").click()

    def logIn(self, token1, token2):
        """
        Fonction permettant de se connecter en arrière plan
        :param token1: nom de compte
        :param token2:  mot de passe du compte
        :return:
        :type token1: String
        :type token2: String
        :rtype: void
        """
        opts = Options()
        opts.set_headless()
        assert opts.headless  # Operating in headless mode
        self.driver = Firefox(
            executable_path=r"\geckodriver.exe",
            options=opts)
        self.driver.implicitly_wait(3)

        # self.driver = webdriver.PhantomJS("phantomjs.exe")
        self.driver.get("https://twitter.com/login")

        username_field = self.driver.find_element_by_class_name("js-username-field")
        password_field = self.driver.find_element_by_class_name("js-password-field")

        time.sleep(2)
        username_field.send_keys(token1)
        self.driver.implicitly_wait(1)

        time.sleep(2)
        password_field.send_keys(token2)
        self.driver.implicitly_wait(1)

        self.driver.find_element_by_class_name("EdgeButtom--medium").click()


    def logIn3(self, token1, token2):
        """
        Fonction permettant de se connecter en arrière plan, avec gestion des erreurs
        :param token1: nom de compte
        :param token2:  mot de passe du compte
        :return:
        :type token1: String
        :type token2: String
        :rtype: void
        """
        opts = Options()
        opts.headless = True
        #opts.set_headless()
        #assert opts.headless  # Operating in headless mode
        try:
            self.driver = Firefox(options=opts)
            self.driver.implicitly_wait(3)
            self.driver.get("https://twitter.com/login")
        except WebDriverException as exception:
            return False
        try:
            username_field = self.driver.find_element_by_class_name("js-username-field")
            password_field = self.driver.find_element_by_class_name("js-password-field")
        except NoSuchElementException as exception:
            return False

        time.sleep(2)
        username_field.send_keys(token1)
        self.driver.implicitly_wait(1)

        time.sleep(2)
        password_field.send_keys(token2)
        self.driver.implicitly_wait(1)

        self.driver.find_element_by_class_name("EdgeButtom--medium").click()

    def checkMainPage(self):
        """
        Fonction de test
        :return:
        :rtype:void
        """
        print(self.main_page)

    def logOut(self):
        """
        Fonction permettant de se déconnecter
        :return:
        :rtype:void
        """
        time.sleep(2)
        self.driver.get(self.main_page)
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/header/div/div/div/div/div[2]/nav/div").click()

        time.sleep(5)
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div/div/div[2]/div[3]/div/div/div/div/div[12]/a").click()

        time.sleep(2)
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath(
            "/html/body/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div[3]/div[2]").click()
        self.driver.close()
        self.driver = ""

    def post(self, message):
        """
        Fonction permettant de poster un message (tweeter)
        :param message: message à tweeter
        :return:
        :type message: String
        :rtype: void
        """
        self.driver.get(self.main_page)
        time.sleep(2)
        self.driver.implicitly_wait(5)

        post_field = self.driver.find_element_by_xpath(
            "/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div")
        self.driver.implicitly_wait(5)
        time.sleep(2)
        post_field.send_keys(message)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath(
            "/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]").click()

    def getPopularTweets(self, theme, number):
        """
        Permet d'obtenir un nombre de tweet populaires sur un thème donné
        :param theme: thème de recherche
        :param number: nombre de derniers tweets à conserver
        :return: les n tweets sous format texte, et le liens vers ceux ci
        :type theme: String
        :type number: int
        :rtype: String
        """
        twitter = Twython(self.APP_KEY, self.APP_SECRET)
        results_popular = twitter.search(q=theme, result_type='popular', count=number)

        all_tweets_popular = results_popular['statuses']

        for tweet2 in all_tweets_popular:
            print(tweet2['text'])

        return results_popular

    def getNotifications(self):
        """
        Permet d'obtenir les dernières notifications
        :return: un texte contenant toutes les dernières noitifications
        :rtype: chaine de caratères
        """
        self.driver.get("https://twitter.com/notifications")
        time.sleep(2)
        url = self.driver.page_source
        # self.driver.save_screenshot("screenshot.png")
        self.driver.implicitly_wait(10)
        element = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/section/div')  # find part of the page you want image of
        location = element.location
        size = element.size
        png = self.driver.get_screenshot_as_png()  # saves screenshot of entire page
        im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save('screenshot.png')
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        text = pytesseract.image_to_string(Image.open('screenshot.png'))
        return text

    def getMentions(self):
        """
        Permet d'obtenir les fois ou on a été mentionné
        :return: un texte contenant toutes les dernières noitifications de mentions
        :rtype: chaine de caratères
               """
        self.driver.get("https://twitter.com/notifications/mentions")
        time.sleep(2)
        url = self.driver.page_source
        # self.driver.save_screenshot("screenshot.png")
        self.driver.implicitly_wait(10)
        element = self.driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div')
        location = element.location
        size = element.size
        png = self.driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save('screenshot.png')
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        text = pytesseract.image_to_string(Image.open('screenshot.png'))
        return text
    # Ne fonctionne pas !
    def getLastTweet(self, author):
        """
        Fonction permettant d'obtenir le dernier tweet d'une personne
        :param author: nom du compte
        :return:
        :type author: String
        :rtype: void
        """
        self.driver.get("https://twitter.com/Win95fr")
        self.driver.implicitly_wait(10)
        ret = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div/div/div[3]/div/article/div/div[2]/div[2]/div[3]/div[2]/div'
        self.driver.find_element_by_xpath(ret).click()

    def verifAccount(self, token1, token2):
        """
        Fonction permettant vérifier qu'un compte existe
        :param token1: nom du compte
        :param token2: mot de passe du compte
        :return:
        :type token1: String
        :type token2: String
        """
        exist = 0
        self.logIn(token1, token2)
        time.sleep(2)
        if self.driver.current_url == self.main_page:
            exist = 1
        return exist



#test = Twitter()
#test.getPopularTweets("python",4)
#test.logIn2("à demander","à demander")
#print(test.getMentions())
# time.sleep(1)
#test.post("Ceci est un message")
#test.post("Ceci est un autre message")
#test.logOut()
# print(test.verifAccount("à demander","à demander"))



"""
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
#TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'

im = Image.open('screenshot.png')  # Ouverture du fichier image

im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')

print(im)
text=pytesseract.image_to_string(Image.open('screenshot.png'))
print(text)"""

# With the Selenium API
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import time


class Facebook:
    """
    Navigateur qui va effecter les actions (on utilise Firefox), vide si inutilisé
    """
    driver = ""
    """
    Page d'accueil du compte (pour uniformiser la deconnexion)
    :type : string
    """
    main_page = ""

    def logIn(self, token1, token2):
        """
        Fonction permettant de se connecter
        :param token1: nom de compte
        :param token2: mot de passe du compte
        :return:
        :type token1: String
        :type token2: String
        :rtype: void
        """
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.facebook.com/login")

        self.driver.implicitly_wait(10)
        username_field = self.driver.find_element_by_xpath('//*[@id="email"]')
        self.driver.implicitly_wait(10)
        password_field = self.driver.find_element_by_xpath('//*[@id="pass"]')
        time.sleep(2)
        username_field.send_keys(token1)
        time.sleep(2)
        password_field.send_keys(token2)

        self.driver.find_element_by_xpath("//*[@id='loginbutton']").click()
        self.main_page = self.driver.current_url
        time.sleep(1)
    def checkMainPage(self):
        """
        Fonction de test
        """
        print(self.main_page)

    def logOut(self):
        """
        Fonction permettant de se déconnecter
        :return:
        :rtype: void
        """
        self.driver.get(self.main_page)
        time.sleep(1)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('// *[ @ id = "pageLoginAnchor"]').click()

        time.sleep(1)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("/html/body/div[10]/div/div/div/div/div[1]/div/div/ul/li[9]").click()
        self.driver = ""
        time.sleep(1)
    def post(self, message):
        """
        Fonction permettant de poster un message sur son mur
        :param message: String
        :return:
        :rtype:void
        """
        self.driver.get("https://www.facebook.com/")
        time.sleep(1)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//*[@name='xhpc_message']").send_keys(message)
        time.sleep(1)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/button").click

    def getNotification(self):
        print("en construction")

    def getFriendsRequest(self):
        print("en construction")

    def acceptFriendRequest(self):
        print("en construction")

    def verifAccount(self, token1, token2):
        """
        Fonction permettant de vérifier qu'un compte existe
        :param token1: login du compte
        :param token2: mot de passe du compte
        :return: 1 si le compte existe, 0 sinon
        :type token1: String
        :type token2: String
        :rtype: int
        """
        exist = 0
        self.logIn(token1, token2)
        time.sleep(2)
        if self.driver.current_url == self.main_page:
            exist = 1
        return exist

test = Facebook()

# adresse test bannie
test.logIn("à demander","à demander")
test.post("Bonjour à tous !")
test.logOut()
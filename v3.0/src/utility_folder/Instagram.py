from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException

class Instagram:

    def __init__(self, email, password):
        """
        Constructeur
        :param email:
        :param password:
        :type email : String
        :type password : Strings
        """
        self.driver = webdriver.Firefox()
        self.email = email
        self.password = password

    def logIn(self):
        """
        Connexion
        :return:
        :rtype: void
        """
        self.driver.get("https://www.instagram.com/accounts/login/")
        self.driver.implicitly_wait(5)
        username_field = self.driver.find_element_by_class_name("pexuQ")
        self.driver.implicitly_wait(10)
        password_field = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")

        time.sleep(2)
        username_field.send_keys(self.email)
        time.sleep(2)
        password_field.send_keys(self.password)
        time.sleep(1)
        self.driver.implicitly_wait(5)

        loginButton = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button")
        loginButton.click()

    def followWithUsername(self, username):
        """
        Pour s'abonner à une personne de nom username
        :param username: nom du compte ou s'abonner
        :type username: String
        :return: rien
        """
        print("https://www.instagram.com/" + username + "/")
        self.driver.get("https://www.instagram.com/" + username + "/")
        time.sleep(2)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
        # self.driver.find_element_by_css_selector('button').click

    def unfollowWithUsername(self, username):
        """
        Pour se désabonner à une personne de nom username
        :param username: nom du compte ou s'abonner
        :type username: String
        :return: echec ou succes
        :rtype: int
        """
        print("https://www.instagram.com/" + username + "/")
        self.driver.get("https://www.instagram.com/" + username + "/")
        time.sleep(2)
        followButton = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]').click()
        """if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.driver.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
            return 1
        else:
            return 0  # echec"""

    def verifUser(self, username):
        """
        Verifie qu'un utilisateur existe
        :param username: nom du compte
        :return: 0 si le compte n'existe pas, 1 sinon
        """
        self.driver.get('https://www.instagram.com/' + username)
        validite = False
        try:
            webElement = self.driver.find_element_by_xpath("/html/body/div/div[1]/div/div/p/a")
            webElement.click()
            #self.driver.self.driver.find_element_by_xpath('/html/body/div/div[1]/div/div/p/a')
        except NoSuchElementException as exception:
            print("Element not found and test failed")
            validite = True
        return validite

    def getUserFollowers(self, username, max):
        self.driver.get('https://www.instagram.com/' + username)
        followersLink = self.driver.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)

        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers

    def search(self, insta):
        """
        Recherche de posts selon le nom de compte
        :param insta: String
        :return:
        :rtype: void
        """
        search_bar = self.driver.find_element_by_xpath("/html/body/span/section/nav/div[2]/div/div/div[2]/input")
        search_bar.send_keys(insta)

    def logOut(self):
        """
        Deconnexion
        :return:
        :rtype: void
        """
        self.driver.implicitly_wait(1000)
        user_info = self.driver.find_element_by_xpath("/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[3]/a")
        user_info.click()
        self.driver.implicitly_wait(1000)

        user_info_parameter = self.driver.find_element_by_xpath(
            "/html/body/span/section/main/div/header/section/div[1]/div/button")
        user_info_parameter.click()

        self.driver.implicitly_wait(1000)
        user_info_parameter_logout = self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div/button[8]")
        user_info_parameter_logout.click()


test = Instagram("à demander", "à demander")
test.logIn()
time.sleep(3)
print(test.verifUser("reagrgerlmadrid"))
#test.followWithUsername("realmadrid")
#time.sleep(3)
#test.unfollowWithUsername("realmadrid")
# test.logOut()

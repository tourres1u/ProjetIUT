import os
import datetime
import time
from Twitter_API import *
from flask import flash
from twilio.rest import Client


class Bot:
    """
    La classe Bot se connecte à l'API Twilio
    """
    liste_tache = dict()
    twitter_instance = Twitter_API()
    account_sid = 'a demander'  # a mettre dans la base de données
    auth_token = 'a demander'
    client = Client(account_sid, auth_token)

    def __init__(self, user_list, password_list, ordre, duree, tasks):
        """
        Ce constructeur prend en parametre une liste d'utilisateurs, une liste de mots de passe, l'ordre et le type de compte
        par utilisateur, la duree de vie du bot en minutes, une liste de taches, qui est un stream() de la base de données
        firestore.
        L'ordre est tres important car determine le type de compte.

        Exemple:

        ordre = ['Twitter', 'Facebook', 'Gmail']
        example_of_users = ['GenZ', 'Boomer', 'Millenials']
        example_of_pass = ['pt', 'pi', 'pg']
        duree = 8
        tasks = firestore_db.collection(<anything>).stream()


        :param user_list:
        :param password_list:
        :param ordre:
        :param duree:
        :param tasks:
        """
        if len(user_list) != len(password_list) != len(ordre):
            raise NameError('Le nombre de comptes ne correspond pas au nombre de mots de passe')
        else:
            self.__usernames = dict(zip(ordre, user_list))
            self.__passwords = dict(zip(ordre, password_list))
            self.suicideDay = duree
            self.tasks = tasks
            self.log = []

    def getUsers(self, account):
        """
        :param account: type de compte (ex: Twitter)
        :return: liste des utilisateurs
        """
        return self.__usernames[account]

    def getPass(self, account):
        return self.__passwords[account]

    def printCredentials(self, account):
        """
        Affiche l'utilisateur associé au type de reseau : ex : Twitter
        :param account: ex: Twitter
        :return: void
        """

        print('________________________')
        print('Compte :' + account)
        print('Username:' + self.__usernames[account])
        print('Password :' + self.__passwords[account])
        print('________________________')

    # def enregistrerTache(self,tache,type_compte):
    # def executerTaches(self)

    def save_to_log(self, task, plateforme):
        """
        Enregistre une tache effectuee dans le log;
        :param task: intitule de la tache
        :param plateforme: reseau social associe
        :return:
        """
        self.log.append("[ Heure: " + str(time.strftime("%I : %M %p", time.localtime(
            time.time()))) + ' | Publication : \"' + task + '\" | Plateforme '
                                                            ': ' + plateforme + ' ]')
        print('Nouvelle tâche rajoutée au log')

    def vivre(self):  # prend en paremetres des minutes
        """
        Fonction a apeller pour démarrer le bot.
        Le bot meurt au bout d'un temps defini en parametres de son constructeur.
        Il va alors chercher dans la base de donnees toutes les taches qu'il doit executer et agir en fonction du type de compte
        Pour le moment, il n'implémente pas encore un module d'IA.
        Les fonctions des autres réseaux twittet, gmail, facebook, etc sont développées en parallele mais ne sont pas
        encore integrees au bot.

        :return: void
        """
        print('Le bot va vivre ' + str(self.suicideDay) + ' minutes')
        heure_depart = time.time()
        expiration = heure_depart + self.suicideDay * 60
        print('Il est ' + str(time.strftime("%I : %M %p", time.localtime(heure_depart))) + ' actuellement')
        print('Le bot prendra fin à ' + str(time.strftime("%I : %M %p", time.localtime(expiration))))

        while time.time() < expiration:

            for task in self.tasks:
                print('Compte : ' + task.get('account') + ' Publication : ' + task.get('text'))

                if task.get('account') == 'Twitter':
                    self.twitter_instance.logIn2("à demander", "à demander")  # à cacher
                    self.twitter_instance.post(task.get('text'))
                    self.twitter_instance.logOut()
                    self.save_to_log(task.get('text'), 'Twitter')
                    flash(self.return_last_action())  # affichage de l'action
                    self.send_sms_notification(self.return_last_action())  # envoi de notification message
                    # task.get().update({"status": "Fini"})

                if task.get('account') == 'Gmail':
                    print("C'est une tâche google")
                    # Code API Gmail à mettre ici

                if task.get('account') == 'Facebook':
                    print("C'est une tâche Facebook")
                    # Code API Facebook à mettre ici
            break

            # action à entreprendre switch case etc en fonction des comptes blabla
            # polymorphisme à respecter

    def send_sms_notification(self, texte):
        """
        Envoie un sms de notification
        :return: 
        """
        print("Je commence à envoyer")
        message = self.client.messages.create(body=texte, from_='num telephone', to='num telephone')
        print("J'ai fini")

        print(message.sid)

    def return_last_action(self):
        """
        :return:  retourne la derniere action realisee par le bot
        """
        if len(self.log) == 0:
            return "Pas encore de tâches dans le log"
        else:
            return self.log[len(self.log) - 1]

    def getNotificationTwitter(self):
        """
        :return: retourne les dernières notifications twitter
        """
        self.twitter_instance.logIn2("à demander", "à demander")
        notifications = self.twitter_instance.getNotifications()
        self.twitter_instance.logOut()
        return notifications

# if __name__ == '__main__':



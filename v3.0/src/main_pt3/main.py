import firebase_admin, string, random, hashlib
from list_email import *
from Bot import *
from Tools.scripts import google
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import login_required, logout_user, current_user, login_user
from Twitter_API import *

cred = credentials.Certificate('./pt3_key.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
table_users = db.collection('users').document('UK91fxA4p7AveCFiE5bq')
app = Flask(__name__)
app.secret_key = 'secret'  # pour que flash puisse marcher
instanceBot = None  # le bot en question
task_iterator = 0


def randomString(length):
    """
    Genere une chaîne de caractère random dont la taille est donnée en parametre
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def encrypt_string(hash_string):
    """
    Crypte une chaîne de caractères en Sha256
    :param hash_string: chaîne a crypter
    :return: chaîne cryptée
    """
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    index:
    Page dans laquelle l'administrateur se connecte.
    :return:
    """
    error = None
    if request.method == 'POST':
        username_digest = encrypt_string(request.form['username'])
        password_digest = encrypt_string(request.form['password'])
        username = db.collection('admin').document('credentials').get().get('username')
        password = db.collection('admin').document('credentials').get().get('password')
        if username_digest != username or password_digest != password:
            error = 'Veuillez contacter les administrateurs'
        else:
            return redirect(url_for('hello_name'))
    return render_template('index.html', error=error)  # to use old page, change to login.html


@app.route('/gmail', methods=['GET', 'POST'])
def recuperer_gmail():
    """
    Route permettant de visualiser tous les mails gmail par label
    :return:
    """
    if request.method == 'POST':
        print("C'est bien une méthode post")
        label = request.form['label']
        print(label)
        gmail = GmailByGoogleApis("à demander")
        mail_label = gmail.getAllMsgByLabels("from:"+label)
        clear_mail = []
        for m in mail_label:
            #help(m) pour avoir la documentation de la classe
            clear_mail.append(m.getMsg())
        return render_template('gmail.html', clear_mail=clear_mail)

    return render_template('gmail.html')


@app.route('/home')
def hello_name():
    """
    Page atteinte apres l'indentification de l'administrateur
    :return:
    """
    try:
        table = table_users.get()
        nom_afficher = table.get('nom')

    except google.cloud.exceptions.NotFound:
        print(u'Missing data')

    # faire une condition, si des comptes existent deja, ne pas afficher le lien d'enregistrement dans l'html
    return render_template('links.html')  # old version is hello.html


@app.route('/tasks', methods=['GET', 'POST'])
def lister_tache():
    """
    Page ou l'utilisateur peut inscrire des taches pour le bot dans la base de donnees
    C'est un formulaire. IMPORTANT : il faut que la table Tasks existe dans la BD même vide
    :return:
    """

    data = []
    tasks = db.collection('Tasks').stream()
    for task in tasks:
        to_add = {"account": task.get('account'), "publication": task.get('text'), "date": task.get('date'),
                  "status": task.get('status')}
        data.append(to_add)
    global task_iterator  # pour utiliser à l'intérieur de la fonction

    if request.method == 'POST':
        print(" C'est bien une méthode post ! ")
        account = request.form['options']
        publication = request.form['textinput']
        date = request.form['date']
        if len(publication) >= 300:
            flash("Le texte à publier est trop long")
            return redirect(url_for('lister_tache'))
        task = {
            'account': account,
            'text': publication,  # rajouter le fichier
            'date': date,
            'status': "En attente",
        }
        task_iterator += 1
        db.collection('Tasks').document('task_' + randomString(5)).set(task)

        flash("Tâche numéro " + str(task_iterator) + " ajoutée dans la base de données. ")
        data = []
        tasks = db.collection('Tasks').stream()
        for task in tasks:
            to_add = {"account": task.get('account'), "publication": task.get('text'), "date": task.get('date'),
                      "status": task.get('status')}
            data.append(to_add)

        return render_template('listetache.html', data=data)

    return render_template('listetache.html', data=data)


@app.route('/showSignUp', methods=['GET', 'POST'])
def showSignUp():
    """
    Page dans laquelle l'utilisateur peut renseigner ces comptes reseaux sociaux
    :return:
    """
    if request.method == 'POST':
        email_t = request.form['input_email_twitter']
        email_f = request.form['input_email_facebook']
        email_g = request.form['input_email_gmail']
        pass_t = request.form['input_pass_twitter']
        pass_f = request.form['input_pass_facebook']
        pass_g = request.form['input_pass_gmail']
        data_g = {
            'email': encrypt_string(email_g),
            'password': encrypt_string(pass_g)
        }
        data_f = {
            'email': encrypt_string(email_f),
            'password': encrypt_string(pass_f)
        }
        data_t = {
            'email': encrypt_string(email_t),
            'password': encrypt_string(pass_t)
        }
        db.collection('Gmail').document('credentials').set(data_g)
        print("Succès Google")
        db.collection('Facebook').document('credentials').set(data_f)
        print("Succès Facebook")
        db.collection('Twitter').document('credentials').set(data_t)
        print("Succès Twitter")
        return render_template('links.html')

    return render_template('signup.html')


@app.route('/interface', methods=['GET', 'POST'])
def hello_user():
    """
    Page dans laquelle l'utilisateur configure et lance le bot
    Encore en développement
    :return:
    """
    if request.method == 'POST':
        if request.form['submit_button'] == 'go':
            user = []
            passw = []
            order = request.form.getlist('accounts')

            for account in order:
                cred = (db.collection(account).document('credentials')).get()
                user.append(cred.get('email'))
                passw.append(cred.get('password'))
            tasks = db.collection('Tasks').stream()  # recuperation des tâches
            print(order)
            print(user)
            print(passw)
            bot_test = Bot(user, passw, order, int(request.form['retrieve']), tasks)
            # bot_test.vivre()
            notifications = bot_test.getNotificationTwitter()

        elif request.form['submit_button'] == 'stop':
            raise Exception('Arreté prématurement')
        return render_template('hello_user.html', notifications=notifications)
    return render_template('hello_user.html')


if __name__ == '__main__':
    app.run(debug=False)

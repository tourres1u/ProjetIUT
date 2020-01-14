 from __future__ import print_function
import pickle
import os.path
import sys
import html
# from html.parser import HTMLParser
# from html.entities import name2codepoint
# import htmlentitydefs
import base64
import email

from apiclient import errors

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class MessageGmail:  # Définition de notre classe Personne
    """Classe définissant un message Gmail
   les attributs:
    - son service
    - son user_id
    - ses labels"""

    def __init__(self, origine, destinataire, date, suject, msg):  # Notre méthode constructeur
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        self._message = {"from": origine, "to": destinataire, "date": date, "suject": suject, "msg": msg}

    def getMsg(self):
        return self._message

    def setMsg(self, value):
        self._message = value

    def print(self):
        print('from : %s', self._message["from"])
        print('to : %s', self._message["to"])
        print('date : %s', self._message["date"])
        print('suject : %s', self._message["suject"])
        print('msg : %s', self._message["msg"])


class GmailByGoogleApis:
    """Classe définissant une interface de Gmail via l'api GoogleApis
   les attributs:
    - son service
    - son user_id
    - ses labels
    - les messages"""

    def __init__(self, user_id):  # Notre méthode constructeur
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """

        self.user_id = user_id

        creds = None
        # The file token.pickle stores the user's access and refresh tokens,
        # and is
        # created automatically when the authorization flow completes for the
        # first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        self._service = service
        self._messages = []

    def getLabels(self):
        """ Retourne tous les labels"""
        results = self._service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return None
        else:
            self.labels = labels
            print('Labels:')
            for label in labels:
                print(label['name'])
            return labels

    def getAllMsgByLabels(self, search=""):
        """ Retourne tous les messages """
        labels = ["INBOX", "CATEGORY_PERSONAL"]
        messages = self._ListMessagesWithLabels(labels, search)
        for m in messages:
            message = self._GetMessage(msg_id=m["id"])
        return self._messages

    def _ListMessagesWithLabels(self, label_ids=[], search=""):
        """List all Messages of the user's mailbox with label_ids applied.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.

      Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
      """
        try:
            # is:important OR from:google
            response = self._service.users().messages().list(userId=self.user_id,
                                                             labelIds=label_ids, q=search).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self._service.users().messages().list(userId=self.user_id,
                                                                 labelIds=label_ids,
                                                                 pageToken=page_token).execute()

                messages.extend(response['messages'])

            return messages
        except errors.HttpError:
            print('An error occurred: ')

    def _GetMessage(self, msg_id):
        """Get a Message with given ID.

          Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

          Returns:
            A Message.
          """
        try:
            message = self._service.users().messages().get(userId=self.user_id, id=msg_id).execute()

            headers = message['payload']['headers']
            # date = headers.find(lambda x: x['name'] == 'Date')[0]
            date = [x for x in headers if x['name'] == 'Date'][0]["value"]
            origine = [x for x in headers if x['name'] == 'From'][0]["value"]
            to = [x for x in headers if x['name'] == 'To'][0]["value"]
            sujects = [x for x in headers if x['name'] == 'Subject']
            if sujects != []:
                suject = sujects[0]["value"]
            else:
                suject = ""

            # test qui ne fonctionne pas pour avoir du texte lisible
            # m = htmlentitydefs.name2codepoint[(message['snippet'])]
            # m = base64.urlsafe_b64decode(message['snippet'])
            # m = html.entities.html5(message['snippet'])
            # m = html.entities.name2codepoint(message['snippet'])
            # m = html.entities.name2codepoint(message['snippet'])
            # --------------------------------------
            # parser = htmlparser.HTMLParser()
            # m = parser.unescape(message['snippet'])
            # m = HtmlParser.init(message['snippet'])

            msgGmail = MessageGmail(origine=origine,
                                    destinataire=to,
                                    date=date,
                                    suject=suject,
                                    msg=message['snippet'])
            msgGmail.print()
            self._messages.append(msgGmail)


        except errors.HttpError:
            print('An error oc')

    def SendMessage(self, message):
        """Send an email message.

          Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

          Returns:
            Sent Message.
          """
        try:
            message = (self._service.users().messages().send(userId=self.user_id, body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError:
            print('An error occurred: %s' % error)

    def CreateMessage(self, sender, to, subject, message_text):
        """Create a message for an email.

          Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

          Returns:
            An object containing a base64url encoded email object.
          """
        message = MIMEText(message_text)

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def CreateMessageWithAttachment(self, sender, to, subject, message_text, file_dir,
                                    filename):
        """Create a message for an email.

      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file_dir: The directory containing the file to be attached.
        filename: The name of the file to be attached.

      Returns:
        An object containing a base64url encoded email object.
      """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        path = os.path.join(file_dir, filename)
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(path, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def Save(self, outfile):
        with open(outfile) as data_file:
            json.dump(self._messages, outfile, ensure_ascii=False, indent=4)


def main():
    gmail = GmailByGoogleApis("à demander")


    messages = gmail.getAllMsgByLabels("from:google")
    for m in messages:
        print('je print')
        m.print()


if __name__ == '__main__':
    main()

import logging
import smtplib
from email.message import EmailMessage
import imaplib
import email


# constantes ########################################################################

NAME_LOG = "journal_main_webhook.log"

# module logging ########################################################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s"
)

file_handler = logging.FileHandler(NAME_LOG)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Fonctions script ####################################################################

####################### ENVOYER EMAIL #########################################


def messenger():

    logger.debug("--------------------------------------------------------")

    try:

        msg = EmailMessage()
        msg["Subject"] = "TESSSSSSSSSSSST"
        msg["From"] = "XXXXXXXXXXXXXXXXX@gmail.com"
        msg["To"] = "XXXXXXXXXXXXXXXX@gmail.com"
        msg.set_content("Hello world")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("XXXXXXXXXXXXXXXXXXXXXX@gmail.com", "XXXXXXXXXXXXXXXXXXXXX")
            smtp.send_message(msg)

        logger.debug("Mail web hook envoyé par robot messenger")
        logger.debug("--------------------------------------------------------")

        return True

    except Exception as e:
        logger.exception(e)
        logger.debug("--------------------------------------------------------")


####################### LIRE/RECUPERER EMAIL #########################################


################################################################


def get_body(msg=None):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def get_last_email():

    try:

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("XXXXXXXXXXXXXXXX@gmail.com", "XXXXXXXXXXXXXXXXXXXXXX")
        mail.list()
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string
        latest_email_id = id_list[-1]  # get the latest
        result, data = mail.fetch(
            latest_email_id, "(RFC822)"
        )  # fetch the email body (RFC822) for the given ID
        raw = email.message_from_bytes(data[0][1])

        return str(get_body(raw))

    except Exception as e:
        return e

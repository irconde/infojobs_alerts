#!/usr/bin/python


from infojobs_handler import InfojobsHandler
import smtplib
from email.mime.text import MIMEText
import sys
import logging
import telebot
from galejobs_handler import GalejobsHandler

MAIL_SENDER = 0
BOT_SENDER = 1

def main():


    logger = logging.getLogger('infojobs_handler')
    hdlr = logging.FileHandler('error.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    num_args = len(sys.argv)

    if num_args == 4:
        sender = BOT_SENDER
    elif num_args == 5:
        sender = MAIL_SENDER
    else:
        logger.error('Incorrect number of input parameters')
        return

    if sender == MAIL_SENDER:

        from_mail = sys.argv[1]
        from_pass = sys.argv[2]
        to_mail = sys.argv[3]
        config_file = sys.argv[4]

    elif sender == BOT_SENDER:

        token = sys.argv[1]
        room_id = sys.argv[2]
        config_file = sys.argv[3]



    # We get a json from Galejobs server with job offers

    galejobs_manager = GalejobsHandler(config_file)
    galejobs_manager.load_config()
    galejobs_manager.query_job_offers()

    if galejobs_manager.offer_list is not None and galejobs_manager.offer_list != []:

        if sender == MAIL_SENDER:
            job_offers = str(galejobs_manager.get_offers_summary())
            msg = MIMEText(job_offers)
            msg['Subject'] = 'Nuevas ofertas de Galejobs'
            msg['From'] = from_mail
            msg['To'] = to_mail

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(from_mail, from_pass)
            server.sendmail(from_mail, [to_mail], msg.as_string())
            server.quit()

        elif sender == BOT_SENDER:
            job_offers = galejobs_manager.get_offers_list()
            infobot = telebot.TeleBot(token)

            for job_offer in job_offers:
                infobot.send_message(room_id, job_offer)



    infojobs_manager = InfojobsHandler(config_file)
    infojobs_manager.load_config()
    infojobs_manager.query_job_offers()

    if infojobs_manager.offer_list is not None and infojobs_manager.offer_list != []:

        if sender == MAIL_SENDER:
            job_offers = str(infojobs_manager.get_offers_summary())
            msg = MIMEText(job_offers)
            msg['Subject'] = 'Nuevas ofertas de InfoJobs'
            msg['From'] = from_mail
            msg['To'] = to_mail

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(from_mail, from_pass)
            server.sendmail(from_mail, [to_mail], msg.as_string())
            server.quit()

        elif sender == BOT_SENDER:
            job_offers = infojobs_manager.get_offers_list()
            infobot = telebot.TeleBot(token)

            for job_offer in job_offers:
                infobot.send_message(room_id, job_offer)


    else:
        logger.info('New jobs not found')


if __name__ == "__main__":
    main()


#!/usr/bin/python


from infojobs_handler import InfojobsHandler
import smtplib
from email.mime.text import MIMEText
import sys
import logging


def main():

    logger = logging.getLogger('infojobs_handler')
    hdlr = logging.FileHandler('error.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    if len(sys.argv) != 5:
        logger.error('Incorrect number of input parameters')
        return

    from_mail = sys.argv[1]
    from_pass = sys.argv[2]
    to_mail = sys.argv[3]
    config_file = sys.argv[4]

    # We get a json from server with job offers

    infojobs_manager = InfojobsHandler(config_file)
    infojobs_manager.load_config()
    infojobs_manager.query_job_offers()

    if infojobs_manager.offer_list is not None and infojobs_manager.offer_list != []:

        msg = MIMEText(str(infojobs_manager.get_offers_summary()))
        msg['Subject'] = 'Nuevas ofertas de InfoJobs'
        msg['From'] = from_mail
        msg['To'] = to_mail

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_mail, from_pass)
        server.sendmail(from_mail, [to_mail], msg.as_string())
        server.quit()
    else:
        logger.info('New jobs not found')

if __name__ == "__main__":
    main()


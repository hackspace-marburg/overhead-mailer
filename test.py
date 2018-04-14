#!/usr/bin/env python

from configparser import ConfigParser

from pmwiki import PmWikiOverheadGrepper

from email.message import EmailMessage
from email.utils import formatdate
from smtplib import SMTP


def send_mail(subject, body):
    ''' Simple function to compose an email with the given subject and body
        based on the config.
    '''
    msg = EmailMessage()
    msg['From'] = conf.get('mail', 'sender_string')
    msg['To'] = conf.get('mail', 'recipient')
    msg['Subject'] = subject
    msg['Date'] = formatdate()
    msg.set_content(body)

    smtp = SMTP(conf.get('smtp', 'server'), conf.getint('smtp', 'port'))
    smtp.starttls()
    smtp.ehlo()
    smtp.login(conf.get('smtp', 'username'), conf.get('smtp', 'password'))
    smtp.send_message(msg)
    smtp.close()


if __name__ == '__main__':
    conf = ConfigParser()
    conf.read('config.ini')

    # TODO: dynamic date
    date = '2018-03-05'
    wiki = PmWikiOverheadGrepper(conf.get('pmwiki', 'domain'))
    data = wiki.get_overhead_topics(date)
    content = PmWikiOverheadGrepper.nested_list_to_str(data)

    mail_subject = conf.get('mail', 'subject_format').format(date)
    mail_body = 'Overhead {}\n\n{}\n\nhttps://{}/Overhead/{}'.format(
      date, content, conf.get('pmwiki', 'domain'), date)

    send_mail(mail_subject, mail_body)

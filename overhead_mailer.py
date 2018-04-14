#!/usr/bin/env python

from configparser import ConfigParser
from datetime import date, timedelta

from pmwiki import PmWikiOverheadGrepper

from email.message import EmailMessage
from email.utils import formatdate
from smtplib import SMTP


def next_overhead_date():
    ''' Calculates the next Overhead's day based on the given day of the week
        in the configuration and the current date.
    '''
    day_of_week = conf.getint('pmwiki', 'day_of_week')
    today = date.today()
    overhead_day = today + timedelta((day_of_week - today.weekday()) % 7)
    return overhead_day.strftime('%Y-%m-%d')


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

    date = next_overhead_date()

    try:
        wiki = PmWikiOverheadGrepper(conf.get('pmwiki', 'domain'))
        data = wiki.get_overhead_topics(date)
        content = PmWikiOverheadGrepper.nested_list_to_str(data)

        mail_subject = conf.get('mail', 'subject_format').format(date)
        mail_body = 'Overhead {}\n\n{}\n\nhttps://{}/Overhead/{}'.format(
          date, content, conf.get('pmwiki', 'domain'), date)

        send_mail(mail_subject, mail_body)
    except Exception as e:
        print('Something went wront: {}'.format(e))

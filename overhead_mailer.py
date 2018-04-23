#!/usr/bin/env python

from argparse import ArgumentParser
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
    parser = ArgumentParser()
    parser.add_argument(
      '-c', '--config', default='config.ini',
      help='path to config (default: config.ini)')
    parser.add_argument(
      '--dry-run', action='store_true',
      help='don\'t send a mail, just print it\'s content')
    parser.add_argument(
      '--date', default=None,
      help='use given date (format %%Y-%%m-%%d) instead of calculated one')
    args = parser.parse_args()

    conf = ConfigParser()
    conf.read(args.config)

    date = args.date if args.date is not None else next_overhead_date()

    try:
        wiki = PmWikiOverheadGrepper(conf.get('pmwiki', 'domain'))
        data = wiki.get_overhead_topics(date)
        content = PmWikiOverheadGrepper.nested_list_to_str(data)

        mail_subject = conf.get('mail', 'subject_format').format(date)
        mail_body = 'Overhead {}\n\n{}\n\nhttps://{}/Overhead/{}'.format(
          date, content, conf.get('pmwiki', 'domain'), date)

        if args.dry_run:
            print('Subject: {}\n\n{}\n'.format(mail_subject, mail_body))
        else:
            send_mail(mail_subject, mail_body)
    except Exception as e:
        print('Something went wront: {}'.format(e))

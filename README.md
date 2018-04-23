# Overhead Mailer
Simple script to send the content of the *Themenliste* (topic list) for the next
Overhead to our mailing list.

## Configuration
Copy `config.example.ini` to `config.ini` and change the content.

## Usage
```
usage: overhead_mailer.py [-h] [-c CONFIG] [--dry-run] [--date DATE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to config (default: config.ini)
  --dry-run             don't send a mail, just print it's content
  --date DATE           use given date (format %Y-%m-%d) instead of calculated
                        one
```

# Overhead Mailer
Simple script to send the content of the *Themenliste* (topic list) for the next
Overhead to our mailing list.

## Configuration
Copy `data/config.example.ini` to `config.ini` and change the content.

## Usage
```
usage: overhead_mailer [-h] [-c CONFIG] [--dry-run] [--date DATE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to config (default: config.ini)
  --dry-run             don't send a mail, just print it's content
  --date DATE           use given date (format %Y-%m-%d) instead of calculated
                        one
```

### NixOS
The Overhead Mailer is also usable as a NixOS module. Modify your
`configuration.nix` as follows:

```nix
{ config, pkgs, ... }:
{
  imports = [
    … 
    path/to/this/repo/default.nix
  ];

  # ...

  services.overhead-mailer = {
    enable     = true;
    configFile = /path/to/the/config.ini;
    interval   = "Thu *-*-* 04:20:00";
  };
}
```

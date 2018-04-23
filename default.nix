{ config, lib, pkgs, ... }:

with lib;

let
  overhead-mailer = pkgs.python36Packages.buildPythonPackage rec {
    name = "overhead-mailer-${version}";
    version = "0.1";

    src = ./.;

    propagatedBuildInputs = [ pkgs.python36Packages.beautifulsoup4 ];
  };

  cfg = config.services.overhead-mailer;
in {
  options.services.overhead-mailer = {
    enable = mkOption {
      type = types.bool;
      default = false;
      description = ''
        If enabled, the overhead mailer will periodically check the
        PmWiki's Overhead and compose a mail to the mailing list.
      '';
    };

    interval = mkOption {
      type = types.str;
      default = "Thu *-*-* 04:00:00";
      description = ''
        Runs the overhead mailer at this interval, by default at 4 AM
        every thursday.

        The format is described in
        systemd.time(7).
      '';
    };

    configFile = mkOption {
      type = types.path;
      description = "Path of the 'config.ini' file.";
    };
  };

  config = {
    systemd.services.overhead-mailer = mkIf cfg.enable {
      description = "Overhead Mailer";
      script = "${overhead-mailer}/bin/overhead_mailer -c ${cfg.configFile}";
    };

    systemd.timers.overhead-mailer = mkIf cfg.enable {
      description = "Overhead Mailer";
      partOf = [ "overhead-mailer.service" ];
      wantedBy = [ "timers.target" ];
      timerConfig.OnCalendar = cfg.interval;
    };
  };
}

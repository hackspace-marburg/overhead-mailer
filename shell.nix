with import <nixpkgs> {};

(pkgs.python36.withPackages (ps: with ps; [ beautifulsoup4 ])).env

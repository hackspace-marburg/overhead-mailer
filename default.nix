with import <nixpkgs> {};
with pkgs.python36Packages;

buildPythonPackage rec {
  name = "overhead-mailer-${version}";
  version = "0.1";

  src = ./.;

  propagatedBuildInputs = [ beautifulsoup4 ];
}

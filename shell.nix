{ pkgs ? import <nixpkgs> {}}:
with pkgs;
mkShell {
    buildInputs = [
        python3
        python39Packages.urllib3
    ];
}
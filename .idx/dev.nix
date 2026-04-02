{ pkgs, ... }: {
  services.docker.enable = true;

  channel = "stable-23.11";

  packages = with pkgs; [
    python3
    gnumake
  ];

  env = {


  };

  idx.workspace.onStart = {
    docker-setup = ''
    '';
  };
}
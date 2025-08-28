{ pkgs }:
{
  deps = [
    pkgs.python3Packages.discordpy
  ];
  env = {.env
  };
}
from fabric.api import local

PEP8_IGNORE = ["E111", "E121", "E261", "E302"]

def pep8(filename="alpha.py"):
  local("pep8 --ignore=" + ",".join(PEP8_IGNORE) + " " + filename)
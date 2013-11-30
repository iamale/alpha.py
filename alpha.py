#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import readline

import texttable
import wolframalpha

# config parsing

import json
from os.path import expanduser

config = {
  'app_id': None
}

try:
  f = open(expanduser('~/.alpharc'))
  config.update(json.loads(f.read()))
except:
  pass

# / config parsing

PROMPT = 'α> '

app_id = config['app_id']
if app_id is None:
  print("app_id isn't configured")
  sys.exit(1)

client = wolframalpha.Client(app_id)

def parsePod(pod):
  d = pod.__dict__
  m = pod.main.__dict__
  return {
    'id': d['id'],
    'title': d['title'],
    'text': pod.text,
    'img': [node for node in m['node'].getchildren()
            if node.tag == 'img']
  }

def parseTable(t):
  lines = [[c.strip() for c in r]
           for r in [r.split("|") for r in p['text'].split("\n")]]

  rows = [line for line in lines if len(line) > 1]
  printAfter = [line[0] for line in lines if len(line) <= 1]

  table = texttable.Texttable()
  table.set_deco(0)

  maxlen = len(max(rows, key=len))
  for row in rows:
    row.extend(["" for i in range(0, maxlen - len(row))])

  table.add_rows(rows, header=False)
  
  return (table.draw() + '\n' + '\n'.join(printAfter))

def printPods(pods):
  for pod in pods:
    p = parsePod(pod)
    if p['text'] is not None:
      print(p['title'])
      print("".join(['=' for _ in p['title']]))
      print("")

      # Pretty-print tables
      if " |" in p['text'] and '\n' in p['text']:
        print(parseTable(p['text']))

      # Pretty-print lists
      elif " |" in p['text']:
        print('\n'.join(["* " + s.strip() for s in p['text'].split("|")]))

      else:
        print(p['text'])

      print("")

def repl():
  try:
    prev_response = None

    while True:
      try:
        s = str(raw_input(PROMPT))
      except EOFError, e:
        print("")
        sys.exit()

      try:
        if s == "??":
          response = prev_response
          printPods(response.pods)

        elif s[0] == "?":
          query = s[1:].strip()
          response = client.query(query)
          printPods(response.pods)

        else:
          query = s.strip()
          response = client.query(query)
          prev_response = response

          no_results = True
          for result in response.results:
            no_results = False
            print(result.text)
            print("")

          if no_results:
            printPods(response.pods)

      except KeyboardInterrupt, e:
        print("Interrupted.")

  except KeyboardInterrupt, e:
    print("")
    sys.exit()

if __name__ == '__main__':
  repl()

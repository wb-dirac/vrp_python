#! /usr/bin/python3
# -*- coding=utf-8 -*-
import cgi
import sys
from importlib import import_module
import json

sys.path.append("..")

print('Content-type: text/plain')
print()

form = cgi.FieldStorage()
m = form.getvalue("m", "main")
f = form.getvalue("f", "main")

module = import_module(m)
fun = getattr(module, f)
res = fun()
print(json.dumps(res))

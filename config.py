#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class Config:
    def __init__(self):
        with open('config.json', 'r') as f:
            data=f.read()
        self._obj = json.loads(data)
        print(self._obj)

    def get(self,k):
        return self._obj[k]

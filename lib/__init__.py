#!/usr/bin/python
# -- module --
from importlib import import_module
from mimetypes import guess_type
from httpx import AsyncClient
from datetime import datetime
from os.path import abspath, exists, getsize, dirname, basename, isfile
from threading import Thread
from shutil import get_terminal_size
from itertools import cycle
from time import sleep, ctime
from bs4 import BeautifulSoup
from glob import glob

class Loader(object):
    def __init__(self, desc: str) -> None:
        self.desc = desc
        self._thread = Thread(target=self.animate, daemon=True)
        self.done = False
        self.times = (lambda : ctime().split()[-2])

    def start(self):
        self._thread.start()
        return self
    
    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(
            f"\r [reuslts]: ....", flush=True
        )

    def animate(self):
        for i in cycle(["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]):
            if self.done:
                break
            print(
                f"\r [{self.times()}] {self.desc} {i}", flush=True, end=""
            )
            sleep(0.05)

class Base(AsyncClient):

    def __init__(self) -> None:
        super().__init__()
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        })
        self.failed = {
            "status": False
        }

    def parse(self, raw):
        return BeautifulSoup(
            raw.text if hasattr(raw, 'text') else raw,
            "html.parser"
        )

    def get_mime(self, fname):
        mime = guess_type(fname)[0]
        if not mime:
            return "application/octet-stream"
        return mime
    
    def format_size(self, size):
        for x in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        return size

    def check_file(self, fname):
        fullpath = abspath(fname)
        if exists(fullpath) and isfile(fullpath):
            return fullpath
        return None
    
    def validDate(self, dates):
        try:
            return datetime.strptime(
                dates.split(
                    '.')[0], "%Y-%m-%dT%H:%M:%S"
                ).strftime("%d %B %Y, %H:%M:%S") 
        except ValueError:
            return None
    
    def check_size(self, fname):
        total = getsize(fname)
        if total > 0x1f400000:
            return None #raise ValueError('file to big')
        return total

basedir = dirname(__file__)
for file in glob(f"{basedir}/*.py"):
    filename = basename(file)[:-3]
    if not filename.startswith('__'):
        import_module(f"lib.{filename}")

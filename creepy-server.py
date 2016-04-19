#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# creepy-server.py for  in /home/grange_c/creepy-server/
#
# Made by Benjamin Grange
# Login   <grange_c@epitech.net>
#
# Started on  Tue Apr 19 00:44:54 2016 Benjamin Grange
#

import os
import sys
import urllib.parse
import socket
import random

__version__ = "0.1.0"

def generate_package_description(path):
        capsule = open(path, "r")
        name = ""
        description = ""
        version = ""
        for line in capsule:
                if line.startswith("name="):
                        name = (line.split("name=")[1])[:-1]
                if line.startswith("version="):
                        version = (line.split("version=")[1])[:-1]
                if line.startswith("description="):
                        description = (line.split("description=")[1])[:-1]
        if (name == "" or version == "" or description == ""):
                return None
        else:
                return name + "|" + version + "|" + description

def generate_package_list():
        ret = ""
        file_content = None
        for root, dirs, files in os.walk("./packages/"):
                for name in files:
                        if name == "CAPSULE.conf":
                                file_content = generate_package_description(os.path.join(root, name))
                                if file_content:
                                        ret += file_content + "\n"
        return ret

def init_server(url):
        print("Launching Creepy-Server v" + __version__ + "... (Address:", url, ")")
        url = urllib.parse.urlparse(url)
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.bind((url.hostname, url.port))
        sk.listen(10)
        print("Done ! Wating for connections...")
        return sk

def main(argv):
        url = argv[0] if (len(argv)) else "http://localhost:8000"
        sk = init_server(url)
        while True:
                conn, addr = sk.accept()
                print ("=== connexion received from", addr, "===")
                request = conn.recv(4096).decode("ISO-8859-1")
                if (request):
                        response = generate_package_list()
                        if response != "":
                                print ("   -> Sending packet list !")
                                conn.sendall(response.encode("ISO-8859-1"))
                        else:
                                print ("   -> An error has occured ! :(")
                                conn.sendall("ERROR 1001".encode("ISO-8859-1"))
                print ("=== ending connexion from", addr, "===")
                conn.close()
        return (0)

if __name__ == '__main__':
        sys.exit(main(sys.argv[1:]))
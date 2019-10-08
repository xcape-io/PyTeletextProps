#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sound.py
MIT License (c) Marie Faure <dev at faure dot systems>

Play audio with aplay (until it ends).
"""

import gettext

try:
    gettext.find("Sound")
    traduction = gettext.translation('Sound', localedir='locale', languages=['fr'])
    traduction.install()
except:
    _ = gettext.gettext  # cool, this hides PyLint warning Undefined name '_'

import os, subprocess


class Sound:

    # __________________________________________________________________
    def __init__(self, logger=None):

        super().__init__()

        self._logger = logger
        self._file = None
        self._player = None

    # __________________________________________________________________
    def play(self, file):

        if self.isPlaying():
            return

        if os.path.exists(file):
            self._file = file
            try:
                self._player = subprocess.Popen(
                    ['aplay', file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
            except Exception as e:
                if self._logger:
                    self._logger.error(_("Sound API : failed to load file"))
                    self._logger.debug(e)
            if self._logger:
                self._logger.info("{} {}".format(_("Sound API : playing"), file))
        else:
            self._file = None
            if self._logger:
                self._logger.info("{} {}".format(_("Sound API : file not found"), file))

    # __________________________________________________________________
    def isPlaying(self):

        if self._player is not None:
            self._player.poll()

            if self._player.returncode is None:
                return True
            else:
                return False

        else:
            return False

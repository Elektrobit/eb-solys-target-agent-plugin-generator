# Copyright 2018, Elektrobit Automotive GmbH. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed with this file, 
# You can obtain one at https://mozilla.org/MPL/2.0/.
# logger.py
from tkinter import *


class Logger:
    def __init__(self, inputText):
        self.inputText = inputText

    def printInfo(self, text_to_display):
        self.inputText.config(state=NORMAL)
        self.inputText.insert(END, "\n" + text_to_display + "\n")
        self.inputText.see(END)
        self.inputText.config(state=DISABLED)

    def printError(self, text_to_display):
        self.inputText.config(state=NORMAL)
        self.inputText.tag_config("n", foreground="red")
        self.inputText.tag_config("Error", background="yellow", foreground="red")
        self.inputText.insert(END, "\n" + text_to_display + "\n", ("n", "a"))
        self.inputText.see(END)
        self.inputText.config(state=DISABLED)

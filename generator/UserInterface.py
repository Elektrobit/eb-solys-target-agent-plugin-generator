# Copyright 2018, Elektrobit Automotive GmbH. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed with this file, 
# You can obtain one at https://mozilla.org/MPL/2.0/.
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from shutil import copyfile
import os
import errno
import sys

from .Logger import Logger
from .UserInput import UserInput
from .InputValidator import InputValidator
from .PluginGenerator import PluginGenerator


class UserInterface(Frame):
    entries = []
    input = None
    eText = None

    def __init__(self):
        Frame.__init__(self)
        self.master.title("Target Agent Plugin Generator")
        self.master.resizable(0, 0)

        self.create_plugin_author_row()
        self.create_plugin_name_row()
        self.create_short_description_row()
        self.create_proto_definition_row()
        self.create_source_folder_row()
        self.create_input_box_row()
        self.create_buttons_row()

    def create_plugin_author_row(self):
        row = Frame(self.master)
        lab = Label(row, width=20, text="Plugin Author", anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        self.entries.append(("Plugin Author", ent))

    def create_plugin_name_row(self):
        row = Frame(self.master)
        lab = Label(row, width=20, text="Plugin Name", anchor='w')
        self.eText = StringVar()
        ent = Entry(row, textvariable=self.eText)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        ent.configure(state='readonly')
        self.eText.set("Plugin name will be extracted from proto file name")
        self.entries.append(("Plugin Name", ent))


    def create_short_description_row(self):
        row = Frame(self.master)
        lab = Label(row, width=20, text="Short plugin Description: ", anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        self.entries.append(("Short plugin Description", ent))

    def create_proto_definition_row(self):
        row = Frame(self.master)
        lab = Label(row, width=20, text="Select Proto definition", anchor='w')
        self.selectedProtoAsText = StringVar()
        selectedProto = Label(row, width=50, textvariable=self.selectedProtoAsText, anchor='w')
        button = Button(row, text="Browse", command=self.load_file, width=5)

        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        selectedProto.pack(side=LEFT)
        button.pack(side=RIGHT, expand=YES, fill=X)

    def create_source_folder_row(self):
        row = Frame(self.master)
        lab = Label(row, width=20, text="Select Ta Source Folder", anchor='w')
        self.selectedPathAsText = StringVar()
        selectedPath = Label(row, width=50, textvariable=self.selectedPathAsText, anchor='w')
        button = Button(row, text="Browse", command=self.askdirectory, width=5)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        selectedPath.pack(side=LEFT)
        button.pack(side=RIGHT, expand=YES, fill=X)

    def create_input_box_row(self):
        row = Frame(self.master)
        self.inputText = Text(row, height=10, width=100, bd=5)

        scroll = Scrollbar(row, command=self.inputText.yview)
        self.inputText.configure(yscrollcommand=scroll.set)
        self.inputText.tag_configure('bold_italics',
                                     font=('Verdana', 12, 'bold', 'italic'))

        self.inputText.tag_configure('big',
                                     font=('Verdana', 24, 'bold'))
        self.inputText.tag_configure('color',
                                     foreground='blue',
                                     font=('Tempus Sans ITC', 14))

        self.inputText.tag_configure('groove',
                                     relief=GROOVE,
                                     borderwidth=2)

        self.inputText.pack(side="top", fill="both", expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        row.pack(side=TOP, fill=X, padx=25, pady=25)
        self.inputText.insert(END, "Target Agent Plugin Generator\n")
        self.inputText.insert(END,
                              "\nThis tool expects amoung others a google protobuf definition having the following name format:\n"
                              "\"target_agent_prot_SampleData_plugin.proto\" where SampleData is the name of the plugin\n."
                              "the plugin skeleton will be generated in the plugins folder of the target agent checkout\n")
        self.inputText.config(state=DISABLED)

    def create_buttons_row(self):
        row = Frame(self.master)
        self.master.bind('<Return>', (lambda event, e=self.entries: self.fetch_input(e)))
        b1 = Button(self.master, text='Generate', command=(lambda e=self.entries: self.fetch_input(e)))
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(self.master, text='Quit', command=self.master.quit)
        b2.pack(side=LEFT, padx=5, pady=5)
        self.logger = Logger(self.inputText)
        self.input = UserInput()

    def load_file(self):
        self.input.protoFile = askopenfilename(filetypes=(("Proto definitions", "*.proto"),
                                                          ("All files", "*.*")))
        if self.input.protoFile:
            try:
                self.logger.printInfo("Proto file definition:\n" + self.input.protoFile)
                self.selectedProtoAsText.set(self.input.protoFile)
                try:
                    self.input.pluginName = re.search('target_agent_prot_(.+?)_plugin', self.input.protoFile).group(1)
                    self.logger.printInfo("Plugin name: " + self.input.pluginName)
                    self.eText.set(""+self.input.pluginName)
                except AttributeError:
                    self.logger.printError("Failed to extract name from proto definition file: expected following naming convention target_agent_prot_(*)_plugin")
                return
            except:
                self.logger.printError("Open Source File : Failed to read file\n" + self.input.protoFile)
            return

    def askdirectory(self):
        dir_opt = {}
        dir_opt['mustexist'] = False
        dir_opt['parent'] = self
        dir_opt['title'] = 'Please select directory'
        self.input.taPath = askdirectory(**dir_opt)
        if self.input.taPath:
            self.logger.printInfo("Target Agent Location\n" + self.input.taPath)
            self.selectedPathAsText.set(self.input.taPath)

    def create_plugin_structure(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def fetch_input(self, entries):
        self.input.author = entries[0][1].get()
        self.input.comment = entries[2][1].get()
        validator = InputValidator(self.input, self.logger)
        logger = Logger(self.inputText)

        if validator.all_fields_are_filled_in() and validator.naming_convention_correct():

            for entry in entries:
                field = entry[0]
                text = entry[1].get()
                logger.printInfo(field + text)

            gen = PluginGenerator(self.input, self.logger)

            gen.createPluginStructure()
            gen.createCmakeConfiguration()
            gen.createCppFiles()
            gen.createCommonDefinitionEntry()
            logger.printError("Generate Completed!")
        else:
            logger.printError("Invalid Input")

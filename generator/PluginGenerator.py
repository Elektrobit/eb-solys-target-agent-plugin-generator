# Copyright 2018, Elektrobit Automotive GmbH. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed with this file, 
# You can obtain one at https://mozilla.org/MPL/2.0/.
# plugin_generator.py

from shutil import copyfile
import os
import errno
import re


class PluginGenerator:
    def __init__(self, user_input, logger):
        self.user_input = user_input
        self.logger = logger

    def createCommonDefinitionEntry(self):
        self.user_input.protoCommonDefinition = self.user_input.taPath + os.path.sep + 'protocol-definitions' + os.path.sep + 'target_agent_prot_common_definitions.proto'
        if os.path.isfile(self.user_input.protoCommonDefinition):
            f = open(self.user_input.protoCommonDefinition, "r")
            contents = f.readlines()
            f.close()

            for index, i in enumerate(contents):
                if 'MSG_TYPE_LAST' in i:
                    lastMessage = i
                    tokens = re.split("=|;", lastMessage)
                    lastEnumId = int(tokens[1])
                    newEnumId = lastEnumId + 1

                    self.logger.printInfo("the last id is %d" + str(int(tokens[1])))
                    self.logger.printInfo("MSG_TYPE_LAST index %d" % index)
                    contents.insert(index,
                                    '	' + 'MSG_TYPE_'+self.user_input.pluginName.upper() + '_PLUGIN' + '  							 =' + str(
                                            lastEnumId) + ';\n')
                    contents.remove(contents[index + 1])
                    contents.insert(index + 1,
                                    "//	MSG_TYPE_LAST  							 =" + str(newEnumId) + ';\n')
                    f = open(self.user_input.protoCommonDefinition, "w")
                    contents = "".join(contents)
                    f.write(contents)
                    f.close()
                    break
        else:
            self.logger.printError("Invalid self.user_input" + "Protocol definition file not found")

    def createCmakeConfiguration(self):
        src = os.path.realpath('generator'+os.path.sep+'utils' + os.path.sep + 'plugin-template') + os.path.sep + 'CMakeListsTemplate.txt'
        dest = self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName +"-plugin"+ os.path.sep + 'CMakeLists.txt'
        self.logger.printInfo("source" + src)
        self.logger.printInfo("dest" + dest)
        copyfile(src, dest)
        self.inplace_change(dest, 'UniquePluginName', self.user_input.pluginName)

    def createCppFiles(self):
        src = os.path.realpath('generator'+os.path.sep+'utils' + os.path.sep + 'plugin-template') + os.path.sep + 'PluginTemplate.cpp'
        dest = self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName +"-plugin"+ os.path.sep + 'src' + os.path.sep + self.user_input.pluginName + 'Plugin.cpp'
        self.logger.printInfo("source: " + src)
        self.logger.printInfo("dest: " + dest)
        copyfile(src, dest)
        self.inplace_change(dest, 'UniquePluginName', self.user_input.pluginName)
        self.inplace_change(dest, 'UniquePluginUpName', self.user_input.pluginName.upper())
        self.inplace_change(dest, '$author$', self.user_input.author)

        src = os.path.realpath('generator'+os.path.sep+'utils' + os.path.sep + 'plugin-template') + os.path.sep + 'PluginTemplate.hpp'
        dest = self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName+"-plugin" + os.path.sep + 'inc' + os.path.sep + self.user_input.pluginName + 'Plugin.hpp'
        self.logger.printInfo("source: " + src)
        self.logger.printInfo("dest: " + dest)
        copyfile(src, dest)
        self.inplace_change(dest, 'UniquePluginName', self.user_input.pluginName)
        self.inplace_change(dest, 'UniquePluginUpName', self.user_input.pluginName.upper())
        self.inplace_change(dest, '$author$', self.user_input.author)
        self.inplace_change(dest, '$comment$', self.user_input.comment)

    def createPluginStructure(self):
        if os.path.isdir(self.user_input.taPath + os.path.sep + 'plugins'):
            self.create_plugin_structure(
                self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName +"-plugin")
            self.create_plugin_structure(
                    self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName +"-plugin"+ os.path.sep + 'gen')
            self.create_plugin_structure(
                    self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName +"-plugin"+ os.path.sep + 'inc')
            self.create_plugin_structure(
                    self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName +"-plugin"+ os.path.sep + 'src')
            self.create_plugin_structure(
                    self.user_input.taPath + os.path.sep + 'plugins' + os.path.sep + self.user_input.pluginName +"-plugin" + os.path.sep + 'test')
        else:
            self.logger.printError("Invalid self.user_input" + "This is not target agent\n" + self.user_input.taPath)

    def create_plugin_structure(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def inplace_change(self, filename, old_string, new_string):
        s = open(filename).read()
        if old_string in s:
            self.logger.printInfo("Replace: " + old_string + "with :" + new_string)
            s = s.replace(old_string, new_string)
            f = open(filename, 'w')
            f.write(s)
            f.flush()
            f.close()
        else:
            self.logger.printError("No occurances of " + old_string + "found")

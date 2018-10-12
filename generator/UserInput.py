# Copyright 2018, Elektrobit Automotive GmbH. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed with this file, 
# You can obtain one at https://mozilla.org/MPL/2.0/.
# user_input.py


class UserInput:
    def __init__(self):
        self._protoFile = None
        self._taPath = None
        self._pluginName = None
        self._author = None
        self._comment = None

    @property
    def protoFile(self):
        return self._protoFile

    @protoFile.setter
    def protoFile(self, value):
        self._protoFile = value

    @protoFile.deleter
    def protoFile(self):
        del self._protoFile

    @property
    def taPath(self):
        return self._taPath

    @taPath.setter
    def taPath(self, value):
        self._taPath = value

    @taPath.deleter
    def taPath(self):
        del self._taPath

    @property
    def pluginName(self):
        return self._pluginName

    @pluginName.setter
    def pluginName(self, value):
        self._pluginName = value

    @pluginName.deleter
    def pluginName(self):
        del self._pluginName

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @author.deleter
    def author(self):
        del self._author

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    @comment.deleter
    def comment(self):
        del self._comment

    @property
    def protoCommonDefinition(self):
        return self._protoCommonDefinition

    @protoCommonDefinition.setter
    def protoCommonDefinition(self, value):
        self._protoCommonDefinition = value

    @protoCommonDefinition.deleter
    def protoCommonDefinition(self):
        del self._protoCommonDefinition

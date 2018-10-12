# Copyright 2018, Elektrobit Automotive GmbH. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed with this file, 
# You can obtain one at https://mozilla.org/MPL/2.0/.
# input_validator.py
import re
import os

class InputValidator:
    def __init__(self, user_input, logger):
        self.user_input = user_input
        self.logger = logger

    def all_fields_are_filled_in(self):
        if (not self.user_input.protoFile) or (not self.user_input.author) or (
                not self.user_input.taPath):
            self.logger.printError("Not all fields are filled in")
            return False
        return True

    def naming_convention_correct(self):
        fileName = self.user_input.protoFile.split(os.path.sep)
        if not re.match("^[A-Za-z0-9_-]*$", self.user_input.pluginName):
            self.logger.printError("Naming not correct")
            return False
        if 'plugin' in self.user_input.pluginName:
            self.logger.printError("Naming not correct")
            return False

        return True

## Copyright (C) LIMSI-CNRS (2014)
##
## contributor(s) : Jorge Gascon, Damien Touraine, David Poirier-Quinot,
## Laurent Pointal, Julian Adenauer, 
## 
## This software is a computer program whose purpose is to distribute
## blender to render on Virtual Reality device systems.
## 
## This software is governed by the CeCILL  license under French law and
## abiding by the rules of distribution of free software.  You can  use, 
## modify and/ or redistribute the software under the terms of the CeCILL
## license as circulated by CEA, CNRS and INRIA at the following URL
## "http://www.cecill.info". 
## 
## As a counterpart to the access to the source code and  rights to copy,
## modify and redistribute granted by the license, users are provided only
## with a limited warranty  and the software's author,  the holder of the
## economic rights,  and the successive licensors  have only  limited
## liability. 
## 
## In this respect, the user's attention is drawn to the risks associated
## with loading,  using,  modifying and/or developing or reproducing the
## software by the user in light of its specific status of free software,
## that may mean  that it is complicated to manipulate,  and  that  also
## therefore means  that it is reserved for developers  and  experienced
## professionals having in-depth computer knowledge. Users are therefore
## encouraged to load and test the software's suitability as regards their
## requirements in conditions enabling the security of their systems and/or 
## data to be ensured and,  more generally, to use and operate it in the 
## same conditions as regards security. 
## 
## The fact that you are presently reading this means that you have had
## knowledge of the CeCILL license and that you accept its terms.
## 

import readline
from . import base
import importlib
import os
import glob
    
class Completer(base.Base):

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        readline.set_completer(self.complete)
        readline.parse_and_bind('tab: complete')

        self._options = {}
        from ...tools.protocol.root import Root
        self._addLevel(self._options, Root)

        self._screenSets = ['Premier', 'Second', 'Troisieme', 'Quatrieme']

        for moduleName in ['Set', 'Get', 'Reload']:
            try:
                lower = moduleName.lower()
                module = importlib.import_module('....tools.protocol.' + lower, __name__)
                self._options[lower] = {}
                self._addLevel(self._options[lower], getattr(module, moduleName))
            except:
                pass

    def _addLevel(self, options, _class):
        forbidden = ['ask', 'getConnection', 'send']
        for methodName in dir(_class):
            if not methodName.startswith('_') and methodName not in forbidden:
                import inspect
                arguments = inspect.getargspec(getattr(_class, methodName))
                arguments = arguments[0]
                try:
                    arguments.remove('self')
                except:
                    pass
                if len(arguments) == 0:
                    options[methodName] = None
                else:
                    options[methodName] = getattr(self, '_process_' + arguments[0])

    def _process_screenSet(self, words):
        try:
            return [s
                    for s in self._screenSets
                    if s and s.startswith(words[0])]
        except IndexError:
            return self._screenSets[:]

    def _process_file(self, words):
        line = readline.get_line_buffer()
        before_arg = line.rfind(" ", 0, readline.get_begidx())
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:readline.get_begidx()]  # fixed portion of the arg
        arg = line[before_arg+1:readline.get_endidx()]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            if path and os.path.isdir(path) and path[-1] != os.sep:
                path += os.sep
            completions.append(path.replace(fixed, "", 1))
        return completions

    def _getMatches(self, words, dictionary):
        if dictionary is None:
            return []
        if hasattr(dictionary, '__call__'):
            return dictionary(words)
        if len(words) == 0:
            return dictionary.keys()
        key = words[0]
        del(words[0])
        if key in dictionary:
            return self._getMatches(words, dictionary[key])
        return [s + ' '
                for s in dictionary.keys()
                if s and s.startswith(key)]

    def complete(self, text, state):
        try:
            response = None
            if state == 0:
                # This is the first time for this text, so build a match list.
                words = readline.get_line_buffer().strip().split()
                self.matches = sorted(self._getMatches(words, self._options))

            # Return the state'th item from the match list,
            # if we have that many.
            try:
                response = self.matches[state]
            except IndexError:
                response = None
            return response
        except:
            self.logger.log_traceback(True)

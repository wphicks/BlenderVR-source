# -*- coding: utf-8 -*-
# file: blendervr/console/__init__.py

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

import sys
from .. import *


def main():
    if not is_console():
        import bge
        bge.logic.endGame()
        sys.exit()

import os


def stripAnchor(anchor, path):
    if path is None:
        return None
    if anchor is not None:
        relpath = os.path.relpath(path, anchor)
        if not relpath.startswith('..'):
            return (relpath, True)
    return (path, False)


def unstripAnchor(anchor, path):
    if path is None:
        return None
    if path[1] and anchor is not None:
        return os.path.join(anchor, path[0])
    return path[0]


if os.environ.get('READTHEDOCS', False) != 'True':
    main()

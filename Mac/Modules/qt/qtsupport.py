# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'Movies.h'		# The Apple header file
MODNAME = 'qt'				# The name of the module
OBJECTNAME = 'Movie'			# The basic name of the objects used here

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
OBJECTTYPE = "Movie"		# The C type used to represent them
OBJECTPREFIX = MODPREFIX + 'Obj'	# The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

includestuff = includestuff + """
#include <%s>""" % MACHEADERFILE + """
"""

Movie = OpaqueByValueType(OBJECTTYPE, OBJECTPREFIX)
TimeValue = Type("TimeValue", "l")
TimeScale = Type("TimeScale", "l")
TimeBaseFlags = Type("TimeBaseFlags", "l")
QTCallBackFlags = Type("QTCallBackFlags", "h")
TimeBaseStatus = Type("TimeBaseStatus", "l")
QTCallBackType = Type("QTCallBackType", "h")
nextTimeFlagsEnum = Type("nextTimeFlagsEnum", "h")
createMovieFileFlagsEnum = Type("createMovieFileFlagsEnum", "l")
movieFlattenFlagsEnum = Type("movieFlattenFlagsEnum", "l")
dataRefAttributesFlags = Type("dataRefAttributesFlags", "l")
playHintsEnum = Type("playHintsEnum", "l")
mediaHandlerFlagsEnum = Type("mediaHandlerFlagsEnum", "l")

RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")
PicHandle = OpaqueByValueType("PicHandle", "ResObj")


class MyObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null Movie");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeMovie(%s);", itselfname)

# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
object = MyObjectDefinition(OBJECTNAME, OBJECTPREFIX, OBJECTTYPE)
module.addobject(object)

# Create the generator classes used to populate the lists
Function = FunctionGenerator
Method = MethodGenerator

# Create and populate the lists
functions = []
methods = []
execfile(INPUTFILE)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in methods: object.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()


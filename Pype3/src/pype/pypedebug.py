# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

"""Debugging tools for python and pype

Author -- James A. Mazer (mazerj@gmail.com)

"""

import sys
import code
import traceback
import types
import string
import os
from guitools import warn

def trace():
	# useful little tool: prints current file & lineno
	import inspect
	print 'TRACE %s:%d' % (
		inspect.getfile(inspect.currentframe().f_back),
		inspect.currentframe().f_back.f_lineno,
		)

def remotedebug():
	# see: http://code.google.com/p/winpdb/
	try:
		import rpdb2
		p = os.popen('echo debug | winpdb -a pypedebug.py', 'w')
		rpdb2.start_embedded_debugger('debug')
		p.close()
	except ImportError:
		pass

def keyboard(banner='Type EOF/^D to continue', builtin=0):
    """Clone of the matlab keyboard() function.

    Drop down into interactive shell for debugging
    Use it like the matlab keyboard command -- dumps you into
    interactive shell where you can poke around and look at
    variables in the current stack frame

    The idea and code are stolen from something Fredrick
    Lundh posted on the web a while back.

    """

    if builtin:
        import pdb
        print '[->pdb]', banner
        pdb.set_trace()
    else:
        # use exception trick to pick up the current frame
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back

        # evaluate commands in current namespace
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)

        code.interact(banner=banner, local=namespace)

def get_exception(show=None):
	"""Get info about where exception came from"""

	type, value, tb = sys.exc_info()
	if show:
		traceback.print_exception(type, value, tb)
	return string.join(traceback.format_exception(type, value, tb))

def get_traceback(show=None):
	"""Stack dump to stdout.

	Collect the current exception information (after catching
	the exception) as a string so it can be reported to the
	user or logged.
	This is an internal function, don't call it directly, use
	the reporterror() function instead.

	Stolen from the Pmw source code.
	"""

	# Fetch current exception values.
	exc_type, exc_value, tb = sys.exc_info()

	# Give basic information about the callback exception.
	if type(exc_type) == types.ClassType:
		# Handle python 1.5 class exceptions.
		exc_type = exc_type.__name__

	# in python-2.5 exc_type is not a string, must be coerced into one..
	msg = []
	msg.append('Exception: %s (%s)\n' % (exc_value, exc_type))

	# Add the traceback.
	stack = traceback.extract_tb(tb)

	depth = 1
	for frame in stack:
		(file, line, fn, text) = frame
		prefix = '>' * depth
		msg.append('%s File "%s", line %s, in %s:\n' % (prefix, file, line, fn))
		msg.append('%s	 %s\n' % (prefix, text))
		depth = depth + 1
	msg = string.join(msg)
	if show:
		sys.stderr.write(msg)
	return msg


def reporterror(gui=True, dbug=False):
	"""Pretty printer for error messages.

	Pretty print a timestamped error message on the console
	or popup a dialog window based on the current exception
	state in the current stack frame.  This is really just
	for debugging.
	"""
	emsg = get_traceback()
	sys.stderr.write(emsg)
	if gui:
		warn('reporterror', emsg, wait=0, astext=1)
	if dbug:
		keyboard()

def ppDict(d):
	"""Pretty print a dictionary
	"""
	ks = d.keys()
	ks.sort()
	for k in ks:
		print '%-20s %15s=<%s>' % (type(d[k]), k, d[k])

def debug(set=None):
	global _DEBUGFLAG

	if set is not None:
		_DEBUGFLAG = set
	else:
		# if DEBUGFLAG's not set, set it to 0...
		try:
			x = _DEBUGFLAG
		except NameError:
			_DEBUGFLAG = 0
		return _DEBUGFLAG


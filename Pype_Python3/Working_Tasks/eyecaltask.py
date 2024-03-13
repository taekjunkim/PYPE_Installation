#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

"""
This is a simple fixation task with 1,5,9 fixation locations
to test how good calibration is. 
For help with other types of control use 
skeleton.py. At startup, to use default parameters hit cancel.

"""

# Standard modules that are imported for every task.
import sys, types
from pype import *
# I use a number of functions from vectorops in one of the reward
# options, so I'm just going to import the whole module.
from vectorops import *
from random import *

def RunSet(app):
	"""
	This is what is run when you hit the 'start' button (set as such in
	the 'main' function, defined at the end of this file).
	"""
	
	# tally collects the results of the last N trials and displays a
	# running tally at the bottom of the main pype control window
	app.tally(clear=1)
	
	# This erases any information printed to the console
	app.console.clear()
	
	# Update the task's representation of all the parameters set in the
	# task parameter table, rig_params and monk_params - always called P
	P = app.params.check(mergewith=app.getcommon())
	# Save this version (in case you've made changes since the last time
	# the .par file was updated).
	app.params.save()
	app.record_note('task_is', __name__)

	# Basic setup stuff, you shouldn't want to change this.
	app.paused = 0
	app.running = 1
	# Makes a little green light/red light on the main pype window
	app.led(1)
	
		# Set various counters and markers in app.globals.  globals is an
	# instance of the Holder class (initialized in function "main,"
	# below), which just lets you store a bunch of variables inside app
	# in a reasonably neat way.
	# - repnum: number of reps completed, 
	# - ncorrect: number of trials correct
	# - ntrials: number of trials completed
	# - seqcorrect: count of how many trials in a row have been correct
	# - uicount: how many trials have been uninitiated (use with uimax)
	app.globals.repnum = -1
	app.globals.ncorrect = 0
	app.globals.ntrials = 0
	app.globals.seqcorrect = 0
	app.globals.uicount = 0
	#positions are 8dva out; 
    zpx = P['mon_dpyw']/2
	zpy = P['mon_dpyh']/2
	shft8dva = int(8*P['mon_ppd']) 
	app.globals.xpos = [0, shft8dva, 0, -shft8dva, 0, shft8dva, \
						-shft8dva, -shft8dva, shft8dva, 0]
	app.globals.ypos = [0, 0, shft8dva, 0, -shft8dva, shft8dva, \
					    shft8dva, -shft8dva, -shft8dva, 0]
############Randomize stimuli
	a = range(5)
    app.globals.stimorder = []
	nct = 0
    while nct < 200:
		shuffle(a)
		app.globals.stimorder = app.globals.stimorder+a
		nct = nct+1
	
#####################################################
	# This plays a standard beep sequence (defined in pype.py) at the
	# start of the task.  Pretty much all tasks use it.
	app.warn_run_start()

	# Calls RunTrial, and calculates a running percentage correct.
	try:
		# I added this to keep a running "recent" percentage correct
		# because perfomance often changes during the task.
		pctbuffer=[0]*50
		
		# Call Run trial only if there are still unshown stimuli in
		# the stimorder buffer
		while app.running and (app.nreps() == 0 or \
			  app.globals.repnum < app.nreps()):
			try:
				# RunTrial is a function defined below that runs a
				# single trial.
				result=RunTrial(app)
			except UserAbort:
				# The escape key will abort a trial while it's running.
				result=None
				pass
			# This if statement avoids a divide-by-zero error if the
			# first trial is aborted before ntrials is incremented
			if app.globals.ntrials > 0:
				# Take the first value off of the pctbuffer
				xxx=pctbuffer.pop(0)
				if result==1:
					# This is a correct trial.  Other possibilities are
					# 0 if error, 'Abort', and None if uninitiated.
					pctbuffer.append(result)
				else:
					pctbuffer.append(0)
				# Average the performance over the past 50 trials.
				if app.globals.ntrials<len(pctbuffer):
					recent=100*app.globals.ncorrect/app.globals.ntrials
				else:
					recent=100*sum(pctbuffer)/len(pctbuffer)
					
			# This call prints the overall and recent perf % to console
			con(app, " %s: %d/%d %.0f%% (recent %.0f%%)" % \
				(now(), \
				 app.globals.ncorrect, app.globals.ntrials, \
				 100.0 * app.globals.ncorrect / app.globals.ntrials, \
				 recent), 'black')
			
	except:
		# If there's an error generated inside the try statement,
		# it drops to here - reporterror tries to exit cleanly instead
		# of crashing the machine.
		reporterror()
	
	# More housekeeping stuff, also shouldn't change.
	app.repinfo()
	app.running = 0
	app.led(0)
	# standard beep sequence when you hit the "stop" button.
	app.warn_run_stop()
	# marks the data file as done so you know everything is complete.
	app.record_done()

	# This is the end of the RunSet function.
	return 1

def RunTrial(app):
	"""
	RunTrial is called by RunSet.  It does housekeeping stuff associated
	with recording behavioral data for an individual trial, and calls the
	_RunTrial function which actually does the stimulus presentation and
	task control. 
	"""
	# On every trial, we check to see if any parameters have been updated
	# while the last trial was running
	P = app.params.check(mergewith=app.getcommon())
	
	# Note the time that the trial started, again explicitly handled
	# in PypeFile class.
	app.record_note('trialtime', (app.globals.ntrials, Timestamp()))
	
	# This call starts the data record for this trial. The datafile will
	# have a 'start' event encoded with timestamp = 0. Also plexon will 
	# have and event encoded
	app.record_start()
	
	# This function will actually do the task control and stimulus display
	# and return its results back here for housekeeping.
	(result, rinfo, rt, P) = _RunTrial(app, P)
	
	# Stop recording for this trial, reset eye trace and signal trial stop
	# to Plexon.  Encode 'stop' in the datafile, which is the very last
	# thing to get timestamped.
	app.record_stop()
	
	# VERY IMPORTANT, this call actually writes all of the info collected
	# in this trial into the datafile.  Don't muck with it.
	app.record_write(rinfo, rt, P, taskinfo=None)
	
	# Check to see whether we've exceeded the max allowable uninitiated
	# trials, and if so, pop up a little warning box that will stall the
	# task until the user clicks it.  Note rinfo is one of the variables
	# returned by _RunTrial.
	if rinfo == UNINITIATED_TRIAL:
		app.globals.uicount = app.globals.uicount + 1
		if app.globals.uicount > P['uimax']:
			warn('Warning',
				 'UI Count exceeded @ %s\nPlease intervene.\n' % now(), wait=1)
			app.globals.uicount = 0
	else:
		# Re-set the uicount after every good trial, so uimax can only
		# be exceeded by a number of ui trials in a row.  Otherwise,
		# the count would be cumulative
		app.globals.uicount = 0
	
	# This is the end of RunTrial.  In RunSet, the call to RunTrial expects
	# the 'result' variable to get returned, and this is how we do that:
	return result

def _RunTrial(app, P):
	"""
	_RunTrial actually does the behavioral control for the task and shows
	whatever stimuli are specified, etc.  This is the meat of the task,
	and this is where you're going to make changes to make the task do
	what you want it to do. 
	"""
	
	# # # # # # # # # # # # # # # # # #
	# General setup stuff
	# # # # # # # # # # # # # # # # # #
	
	# The intertrial interval is at the start of each trial
	# (arbitrary).  Calling encode will make a note in the data record
	# with the current timestamp and whatever comment you give it.
	app.encode(START_ITI)
	app.encode_plex(START_ITI)

	# Create instances of Timer class (also in pype.py), which counts 
	# milliseconds until it's reset. Can be queried without reset
	t = Timer()
	t.reset()
	t2 = Timer()
	
	# Draw a line at the beginning of every trial
	con(app,">---------------------------")
	# You can write anything you want to the console, and in color.
	con(app,"Next trial",'blue')
	
	# Initialize default reaction time in case trial is aborted
	rt = -1
	
	# Check for "testing" mode (rig params table; no eye or bar monitoring)
	TESTING = int(P['testing'])
	if TESTING:
		# put a big red note on the console so I don't forget
		con(app, 'TESTING','red')
	
	# Clear the user display before starting
	app.udpy.display(None)
	
	# The dlist manages what gets shown on the screen, it gets
	# re-initialized every trial.  app.fb is the framebuffer
	app.globals.dlist = DisplayList(app.fb)
	# set the background color - in this case, I've got a color defined
	# for the intertrial interval
	app.globals.dlist.bg = P['bg_before']
	
	# Update the dlist and flip the framebuffer
	app.globals.dlist.update()
	app.fb.flip()
	# At this point, screen color is bg_before, and otherwise blank.
	
	# # # # # # # # # # # # # # # # # #
	# Code for making a fixation spot
	# # # # # # # # # # # # # # # # # #
	
	# Locate 
	trnum = app.globals.ncorrect%P['num_loc']
	### this is for randomizing
	#trnum = app.globals.stimorder[app.globals.ncorrect]
	fx, fy = app.globals.xpos[trnum], app.globals.ypos[trnum]

	# Set a value in the parameter table, so that it gets recorded in
	# the data file.  NOTE, this value may be *different* from P['fix_x']
	# and P['fix_y'] from the monk_params table, see comment above.
	P['fx'], P['fy'] = fx, fy
	# I'm not clear on what this does, but it has something to do with
	# aligning the user display, and you need it.
	app.looking_at(fx, fy)

	# Here is some basic fixation point code. It either makes a dot
	# or a dot surrounded by a black ring. Note that fix_size and 
	# fix_ring are from monk_params, but fixspot color has to be 
	# specified by the task.
	
	if P['fix_ring'] > 0:
		# Create the sprite
		spot = Sprite(2*P['fix_ring'], 2*P['fix_ring'],
					  fx, fy, fb=app.fb, depth=1, on=0, centerorigin=1)
		# fill the square with bg color
		spot.fill(P['bg_during'])
		# make a black circle of radius fix_ring at the center of the
		# sprite
		spot.circlefill((1,1,1), r=P['fix_ring'], x=0, y=0)
		# and now for the actual fixation point...
		if P['fix_size'] > 1:
			# make another circle of radius fix_size
			spot.circlefill(P['fixcolor1'], r=P['fix_size'], x=0, y=0)
		else:
			# just color the center pixel - r=1 doesn't work well
			spot[0,0] = P['fixcolor1']
	else:
		# Create a sprite without the surrounding ring
		spot = Sprite(2*P['fix_size'], 2*P['fix_size'],
					  fx, fy, fb=app.fb, depth=1, on=0, centerorigin=1)
		spot.fill(P['bg_during'])
		if P['fix_size'] > 1:
			spot.circlefill(P['fixcolor1'], r=P['fix_size'], x=0, y=0)
		else:
			spot[0,0] = P['fixcolor1']
	
	# This is redundant with on=0 above, but make sure the sprite is off
	spot.off()
	# Add spot to the dlist
	app.globals.dlist.add(spot)
	
	# # # # # # # # # # # # # # # # # #
	# Code for making the fixation window
	# # # # # # # # # # # # # # # # # #
	
	# This is the virtual boundary that defines a "good" fixation,
	# again only necessary if yours is a fixation task.
	
	# Adjust fixation window size for target eccentricity, since it's
	# harder to fixate on more eccentric points and there's more
	# eye tracker error too.  The min and max error parameters are
	# task-specific.
	min_e, max_e = P['min_err'], P['max_err']
	r = ((fx**2)+(fy**2))**0.5
	z = min_e + (max_e - min_e) * r / ((app.fb.w+app.fb.h)/2.0)
	# Set a parameter value that's the actual window size to use
	# this trial, so it's saved in data file.
	P['_winsize'] = int(round(P['win_size'] + z))
	
	# Create an instance of the FixWin class (defined in pype.py) that
	# will actually keep track of the eye position for you
	fixwin = FixWin(fx, fy, P['_winsize'], app)
	fixwin.draw(color='grey') #draws the fixwin radius on user display

	# # # # # # # # # # # # # # # # # #
	# Initiate the trial
	# # # # # # # # # # # # # # # # # #

	# Start monitoring the eye trace.  This encodes an 'eye_start' event
	# in the datafile that will always be equal to the first timestamp
	# at which eyetrace data are collected.
	app.eyetrace(1)
	app.encode_plex(EYE_START)
	# set background color to the color defined for during the trial
	app.globals.dlist.bg = P['bg_during']
	app.globals.dlist.update()
	
	# Note that we haven't flipped the framebuffer yet...
	
	# We put the entire trial inside a try statement 
	# with exceptions to stop trial(correct, incorrect, aborted).
	try:
		# The idlefn method just lets the program do background
		# maintenance stuff.  You can give idlefn an argument that
		# specifies a number of milliseconds to wait
		# Timer t was set at the very beginning of the trial,
		# I want to know how long it's been since then.)
		app.idlefn(P['iti']-t.ms())
		app.encode(END_ITI) 
	    app.encode_plex(END_ITI)
        #remember we already encoded START_ITI
		# Some subjects find this helpful, some users find it annoying.
		# I set a flag that lets you use the start tone or not.
		if P['trial_tone']:
			# standard tone at the start of every trial
			app.start_tone()
		
		# Reset this timer to zero
		t.reset()
		
		# Flip the framebuffer to show the current dlist
		app.fb.flip() ### bg color is bg_during
	    
		fixwin.draw(color='red')
		ttt = fixwin.on()
		print "ttt %d %d " % (ttt, t.ms())
		#while not ttt:
		#	print "%d  " % (t.ms())
		
		spot_on=0
		# When we get here either the bar has been grabbed or we're not
		# monitoring it.  If the fixation point is not already
		# on, we'll turn it on now.
		if not spot_on:
			spot.on()
			app.globals.dlist.update()
			app.fb.flip()
			app.encode(FIX_ON)
			app.encode_plex(FIX_ON)
			app.udpy.display(app.globals.dlist)
			spot_on=1
		# Now we're waiting for the subject to acquire the fixation point
        print"spot_on %d %d " % (spot_on,t.ms())
		info(app, "waiting fix acquisition")
	    app.idlefn()
		t.reset()
		
		# Again, a dummy flag to help with task control
		go_on = 0
		while not go_on:
			# We are waiting for the eye position to move inside the
			# fixation window.  Whether this is the case is one of
			# the things that the FixWin class keeps track of.
			while not fixwin.inside() and not TESTING:
				# We use the same abortafter limit again
				if P['abortafter'] > 0 and t.ms() > P['abortafter']:
					info(app, "no acquisition")
					con(app, "no acquisition", 'blue')
					rinfo = UNINITIATED_TRIAL
					app.encode_plex(UNINITIATED_TRIAL)
					beep(2000,100)
					raise MonkError
				app.idlefn()
			# At this point, the fixwin.inside returned 1 (meaning eye
			# is inside window).  Sometimes if the spot has just come
			# on and the subject is in the process of saccading across
			# the screen, the eye position will go through the fixwin.
			# Only count this as acquiring fixation if the eye stays in
			# the window for "fixwait" milliseconds.
			t2.reset()
			# First, assume we will continue if eye stays in window
			go_on = 1
			while t2.ms() < P['fixwait']:
				if not fixwin.inside() and not TESTING:
					# If at any time during the fixwait the eye
					# moves back out of the window, go back to waiting
					# for the eye to enter the window again.
					info(app, "passthrough")
					go_on = 0
					# This resets fixwin.inside back to zero
					fixwin.reset()
					# This exits the innermost while loop, and sends
					# us back to the top of the "while not go_on"
					# loop
					break

		# # # # # # # # # # # # # # # # # #
		# Do real trial stuff
		# # # # # # # # # # # # # # # # # #
	
		# Now, fixation has been acquired.  We can start timing the
		# length of the fixation.
		t.reset() # Reset the timer to monitor fixation length
		app.encode(FIX_ACQUIRED) # Standard event encoding
		app.encode_plex(FIX_ACQUIRED)
		fixwin.draw(color='blue') # Blue is our "active" fixwin color


		# wait for hold time
		t.reset()
		while t.ms() < P['hold']:
		    if fixwin.broke() and not TESTING:
			    app.encode(FIX_LOST) #standard event code
				app.encode_plex(FIX_LOST)
				info(app, "early break")
				con(app, "early break (%d ms)" % t.ms(), 'red')
			   	app.encode('exact_fix_lost=%d' % fixwin.break_time())
				rinfo = BREAK_FIX
			   	app.warn_trial_incorrect(flash=None)
			   	# Skip to end of trial
			   	raise MonkError
			# Again, a call to idlefn lets the computer catch up
		   	# and monitor for key presses.
		   	app.idlefn()
		
################################
		# If you are here then the trial is correct
		raise NoProblem

	# # # # # # # # # # # # # # # # # #
	# Handling exceptions generated in the trial
	# # # # # # # # # # # # # # # # # #
	
	except UserAbort:
		# If you pressed the escape key at any time to abort the trial
		# you will end up here.  No counters are incremented or
		# reset basically because this was not the subject's fault.
		con(app, "Aborted.", 'red')
		# These variables will be returned to RunTrial.
		rinfo = USER_ABORT
		app.encode_plex(USER_ABORT)
		result = 'abort'
	except MonkError:
		# Any of the MonkError exceptions will land you here.  The
		# trial counter is incremented and the seqcorrect counter
		# is reset.
		app.globals.ntrials = app.globals.ntrials + 1
		app.globals.seqcorrect = 0
		# result will be returned to RunTrial.  rinfo is set for
		# each individual error type.
		result = 0
	except NoProblem:
		# Having an exception for a correct trial is handy because
		# there are a number of ways of getting the trial correct
		# depending on whether we're monitoring the eye position or
		# touch bar or dot dimming, and we can put all the reward
		# code in one place.

		#clear after fixation
		app.udpy.display(None)
		app.globals.dlist = DisplayList(app.fb)
		app.globals.dlist.bg = P['bg_before']
		app.globals.dlist.update()
		app.fb.flip()

		rinfo = CORRECT_RESPONSE
		app.encode_plex(CORRECT_RESPONSE)
		app.warn_trial_correct() #Standard "correct" beep
		app.encode(REWARD)
		app.encode_plex(REWARD)
		# Increment the sequence correct counter
		app.globals.seqcorrect=app.globals.seqcorrect + 1
		
		# Without arguments this call dispenses a reward of size
	    # 'dropsize' with a variance of 'dropvar' (both specified
		# in monk_params). The multiplier argument multiplies the
		# "standard" reward by whatever value is passed in.
		clk_num = P['numdrops']
		while clk_num > 0:
			app.reward(multiplier=P['rmult'])
			app.idlefn(50)#time between juice drops
			clk_num = clk_num-1
					
		# Reporting stuff, variables returned to RunTrial
		rinfo = CORRECT_RESPONSE
		app.globals.ncorrect = app.globals.ncorrect + 1
		app.globals.ntrials = app.globals.ntrials + 1
		result = 1

	
	# # # # # # # # # # # # # # # # # #
	# Cleanup
	# # # # # # # # # # # # # # # # # #
	
	# This code runs no matter what the result was, it is after all the
	# exception handling

	# Turn off the fixation spot and tracker dot
	spot.off()
	app.encode(FIX_OFF)
	app.encode_plex(FIX_OFF)
	# Stop monitoring eye position, encode 'eye_stop' in the datafile
	# which will always be the last timestamp at which eyetrace data
	# were collected.
	fixwin.clear()
	app.eyetrace(0)
	app.encode_plex(EYE_STOP)
	# Re-set the background for the intertrial interval
	app.globals.dlist.bg = P['bg_before']
	app.globals.dlist.update()
	app.fb.flip()
	# Clear the user display
	app.udpy.display(None)

	# update behavioral history log on GUI window
	app.history(rinfo[0])

	# If this was an incorrect trial, wait for the timeout period
	# (we do this now so that everything has been shut off and the
	# background is not the "active" color during the timeout
	# period).
	if result == 0:
		if P['timeout'] > 0:
			info(app, "error timeout..")
			app.idlefn(ms=P['timeout'])
			info(app, "done.")

	# Don't know what this does.  Don't touch.
	app.looking_at()
	
	# Update the performance tally on the pype control window.
	app.tally(type=rinfo)

	# Return variables to RunTrial for housekeeping.
	return (result, rinfo, rt, P)

def main(app):
	"""
	Every python program with multiple functions needs to have a main
	function.  This sets up the parameter table, initializes app.globals,
	and defines RunSet as the start function.  You will need to mess
	with the parameter table to add new parameters for your task and
	remove useless ones, but beyond that don't change things in this
	function unless you're *really* sure you know what you're doing.
	"""

	# Initialize things
	app.globals = Holder()
	app.idlefb()
	app.startfn = RunSet
	app.mybutton = app.taskbutton(text=__name__, check=1)
	app.notebook = DockWindow(title=__name__, checkbutton=app.mybutton)
	parfile = app.taskname()
	# Look for an existing saved parameter file for this task
	if parfile:
		parfile = parfile + '.par'

	# Initialization and default values for the parameters.  Each row is
	# one parameter.  The first value is the name of the parameter, the
	# second is its default value, the third defines the type of
	# the value (more on that later) and the fourth is optional and
	# is a descriptive label that pops up when you hold the mouse over
	# that entry in the table.  There are numerous standard parameter
	# types, the most common are self-explanatory.  is_color needs to be
	# 3 or 4 numbers in tuple format, e.g. (255,1,1) for red; the 4th
	# number is optional and is an alpha value (if left off, assumed
	# to be 255).  (0,0,0) is a special code for transparent or for
	# white noise fill pattern, depending on the task, so use (1,1,1)
	# for black.  is_any just gets passed as a string, this is what
	# to use if you need a list of numbers.  is_iparam can take a
	# variance value as either a percentage or an actual number of
	# units, so you'd have "1000+-10%" or "150+-50".  There are a ton of
	# others defined in ptable.py.  Values of None for default value and
	# type make that row into a heading of sorts that can be helpful for
	# organizing a large number of parameters.
	
	app.params = ParamTable(app.notebook, (
		("Subject Params", None, None),
		("usebar",	    "1",		   	is_boolean,),
		("trial_tone",	"1",		   	is_boolean, "tone at every trial"),
		("grabbeep",	"1",		   	is_boolean, "beep at bar grab"),
		("barfirst",	"1",		   	is_boolean, "grab bar before fixspot"),
		("Reward Params", None, None),
		("numdrops",    "15",           is_int, "Number of juice drops"),
		("rmult",		"1.0",		   	is_float),
		("seqcor",      "2",            is_int),
		("seqcor_reset","1",            is_boolean),
		("allornone",   "1",            is_float, "0->1, prob of drop"),
		("Dot Dimming Params", None, None),
		("dim",	        "1",			is_boolean, "do dot dimming?"),
		("fixcolor1",	"(255,255,255)",is_color),
		("fixcolor2",	"(128,128,128)",is_color),
		("maxrt",       "500",          is_int),
		("Task Params", None, None),
		("num_loc", "5",            is_int, "Number of fixation locations"),
		("hold",	"2000",		   	is_int, "Fixation time"),
		("min_err",		"0",		   	is_int),
		("max_err",		"100",		   	is_int),
		("bg_before",	"(1,1,1)",	   	is_color),
		("bg_during",	"(128,128,128)",is_color),
		("fixlag",		"50",		   	is_int),
		("fixwait",		"100",		   	is_int),
		("Eye Params", None, None),
		("innerwin",	"0",		   	is_int),
		("track",		"0",		   	is_boolean),
		("track_xo",   	"0",		   	is_int, "offset of track point"),
		("track_yo",   	"0",		   	is_int, "offset of track point"),
		("track_color", "(255,255,0)", 	is_color),
		), file=parfile)

		
def cleanup(app):
	"""
	This is not run from within the program anywhere, but I believe
	it is necessary because every task has one.  Perhaps it is called
	by pype itself when the task is unloaded.
	"""
	app.params.save()
	app.mybutton.destroy()
	app.notebook.destroy()
	# The dlist should get deleted as part of cleanup, or else all
	# the sprites remain in memory when the task is unloaded.  In
	# this task dlist is part of app.globals.  In tasks where users
	# have chosen not to use app.globals, they need to add a line
	# here to delete the dlist explicitly.
	del app.globals


# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
	loadwarn(__name__)
else:
	dump(sys.argv[1])

# kitten math game

import random
import time

import Tkinter as tk
import tkFont as tkf



class App(tk.Frame):
	"""Application (tk-wise) for the game"""

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)			# initialize superclass
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)	# ensure the window is shown, using the grid manager
		self.Populate()							# create widgets

		# configure so that things have a min size, and will stretch

		top = self.winfo_toplevel()
		top.columnconfigure(0, weight=1)
		top.rowconfigure(0, weight=1)

		self.columnconfigure(0, minsize=30, pad=10, weight=1)
		self.columnconfigure(1, minsize=30, pad=10, weight=0)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=0)

		self.Setup()

	def Setup(self):
		"""Finish setting things up so they'll operate properly"""

		self.afterId = None
		self.answerPending = None
		self.answerWant = None

		self.fileLog = None

		self.kittensRescued = 0
		self.kittenPenalty = 0

		self.problem = ''

		self.timeStartProblem = 0

	def Populate(self):
		"""Create widgets for the window"""

		# establish the font we want to use (bigger than default, to be easier to read)

		fontBig = tkf.Font(family='FreeSans', size=24, weight='normal')

		pady = 10
		iRow = 0

		# quit button

		buttonQuit = tk.Button(self, text='Quit', command=self.OnQuit, font=fontBig)
		buttonQuit.grid(row=iRow, column=0, pady=pady)

		# go/stop button

		buttonPlay = tk.Button(self, text='Play', command=self.OnPlay, font=fontBig)
		buttonPlay.grid(row=iRow, column=1, pady=pady)
		self.buttonPlay = buttonPlay

		iRow += 1

		# label for kittens last saved

		labelLast = tk.Label(self, text='', font=fontBig)
		labelLast.grid(row=iRow, column=0, sticky=tk.E, pady=pady)
		self.labelLast = labelLast

		# label for total kittens saved

		labelTotal = tk.Label(self, text='0 Kittens Saved', font=fontBig)
		labelTotal.grid(row=iRow, column=1, sticky=tk.E, pady=pady)
		self.labelTotal = labelTotal

		iRow += 1

		# label for the timer

		labelTimer = tk.Label(self, text='Kittens Left:', font=fontBig)
		labelTimer.grid(row=iRow, column=0, sticky=tk.E, pady=pady)	# left-most column, right-aligned

		# label for the actual time count

		labelTime = tk.Label(self, text='20', font=fontBig)
		labelTime.grid(row=iRow, column=1, sticky=tk.W, pady=pady)		# right-most column, left-aligned
		self.labelTime = labelTime

		iRow += 1

		# current problem

		labelProblem = tk.Label(self, text='problem', font=fontBig)
		labelProblem.grid(row=iRow, column=0, sticky=tk.E+tk.W, pady=pady)
		self.labelProblem = labelProblem

		# text entry

		sv = tk.StringVar()
		entry = tk.Entry(self, textvariable=sv, font=fontBig)
		entry.grid(row=iRow, column=1, sticky=tk.E+tk.W, pady=pady)
		entry.bind('<KeyPress-Return>', self.OnEnter)
		entry.bind('<KeyPress-KP_Enter>', self.OnEnter)
		entry.focus_set()
		self.entry = entry
		self.sv = sv

		if False:
			# debug block to show font information
			print "All families:"
			print '\n'.join(sorted(tkf.families()))
			print "entry font: ", entry['font']
			print "label font: ", labelProblem['font']

			for family in ['FreeSans', 'Nimbus Sans L', 'TkTextFont', 'Liberation Sans', 'Cantarell']:
				iRow += 1
				label = tk.Label(self, text='Kitten Example {} {}'.format(iRow, family), font=tkf.Font(family=family, size=24, weight='normal'))
				label.grid(row=iRow, column=0, sticky=tk.W)


	def OnQuit(self, *lArg):
		self.quit()

	def OnEnter(self, *lArg):
		if self.afterId is not None:
			self.answerPending = self.sv.get()
			if self.answerPending.strip() == '':
				self.answerPending = None

		self.sv.set('')

	def OnPlay(self, *lArg):

		if self.buttonPlay['text'] == 'Play':
			# start the game

			self.OnTimer()

			# swap the button text to indicate you can stop

			self.buttonPlay['text'] = 'Stop'

		else:
			# stop the game by canceling the afterId

			if self.afterId is not None:
				self.after_cancel(self.afterId)

			# hide the problem

			self.labelProblem.configure(text='problem')

			# clear any pending answers

			self.answerPending = None

			# set up so resume will throw away existing problem and make a new one

			self.timeStartProblem = 0

			# swap the button text to indicate you can play

			self.buttonPlay['text'] = 'Play'

	def OnTimer(self, *lArg):
		"""Run the game logic update, and schedule another such event"""

		timeNow = time.time()

		# handle an answer, if one is available

		if self.answerPending != None:

			# consume and convert to integer

			try:
				answer = int(self.answerPending)
			except:
				answer = -1

			self.answerPending = None

			# check if it is correct for the problem or not

			if answer == self.answerWant:
				# increment number of kittens saved

				kittens = self.KittensRescuable(timeNow)
				self.kittensRescued += kittens

				# update labels

				self.labelLast.configure(text='{k} Last Saved'.format(k=kittens))
				self.labelTotal.configure(text='{k} Kittens Saved'.format(k=self.kittensRescued))

				# record time spent figuring out this answer

				timeSpent = timeNow - self.timeStartProblem
				self.Log(timeSpent)

				# reset to no kitten penalty and reset the start time; that will later cause
				#  a new problem to be created

				self.kittenPenalty = 0
				self.timeStartProblem = 0

			else:
				# decrement available kitten count by a bit

				self.kittenPenalty += 1

				# TODO: maybe turn text red for a bit?

		# see if we need to generate a new problem

		if self.KittensRescuable(timeNow) < 1:

			# reset pentalties and start time

			self.kittenPenalty = 0
			self.timeStartProblem = timeNow

			# generate new problem and desired answer text

			# TODO: take into account history once we have it to steer more towards
			#  problems that are more difficult for the player

			# TODO: consider if we don't want to allow back-to-back same answers;
			#  that's a little less clear than back-to-back same problems, which is
			#  really confusing (looks like you did it wrong)

			problemNext = self.problem
			while problemNext == self.problem:
				a = random.randint(1, 12)
				b = random.randint(1, 9)
				problemNext = '{a} x {b}'.format(a=a, b=b)

			self.problem = problemNext
			self.answerWant = a * b
			self.labelProblem.configure(text=self.problem)

		# update remaining kitten label

		kittens = self.KittensRescuable(timeNow)
		self.labelTime.configure(text='{k}'.format(k=kittens))

		# schedule next update -- striving for about 10 updates per second

		self.afterId = self.after(100, self.OnTimer)

	def KittensRescuable(self, timeNow):
		"""Calculate how many kittens are rescuable at this point"""

		# max kittens: 20, for the first 6-ish seconds; after, decrease by one per 3 seconds,
		#  and lose one kitten per wrong answer

		kittens = int(20 - max(0, timeNow - self.timeStartProblem - 2.0) // 2 - self.kittenPenalty)
		kittens = max(0, kittens)
		return kittens

	def Log(self, timeSpent):
		"""Add a log entry with information about the solution, etc."""

		if self.fileLog is None:
			self.fileLog = open('log.txt', 'a')
			self.fileLog.write('== new session ==\n')

		self.fileLog.write('{prob}, {ans}, {time}, {penalty}, {score}\n'.format(
							prob=self.problem,
							ans=self.answerWant,
							time=timeSpent,
							penalty=self.kittenPenalty,
							score=self.kittensRescued))

def Main():
	"""Main driver for kitten game"""

	app = App()
	app.master.title('Kitten Math')
	app.mainloop()



if __name__ == '__main__':
	Main()

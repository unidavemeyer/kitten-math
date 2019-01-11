# kitten math game

import Tkinter as tk



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

	def Populate(self):
		"""Create widgets for the window"""

		iRow = 0

		# quit button

		buttonQuit = tk.Button(self, text='Quit', command=self.OnQuit)
		buttonQuit.grid(row=iRow, column=0)

		iRow += 1

		# label for kittens last saved

		labelLast = tk.Label(self, text='')
		labelLast.grid(row=iRow, column=0, sticky=tk.E)
		self.labelLast = labelLast

		# label for total kittens saved

		labelTotal = tk.Label(self, text='0 Kittens Saved')
		labelTotal.grid(row=iRow, column=1, sticky=tk.E)
		self.labelTotal = labelTotal

		iRow += 1

		# label for the timer

		labelTimer = tk.Label(self, text='Kittens Left:')
		labelTimer.grid(row=iRow, column=0, sticky=tk.E)  # left-most column, right-aligned

		# label for the actual time count

		labelTime = tk.Label(self, text='20')
		labelTime.grid(row=iRow, column=1, sticky=tk.W)   # right-most column, left-aligned
		self.labelTime = labelTime

		iRow += 1

		# current problem

		labelProblem = tk.Label(self, text='6 x 7')
		labelProblem.grid(row=iRow, column=0, sticky=tk.E+tk.W)
		self.labelProblem = labelProblem

		# text entry

		sv = tk.StringVar()
		entry = tk.Entry(self, textvariable=sv)
		entry.grid(row=iRow, column=1, sticky=tk.E+tk.W)
		entry.bind('<KeyPress-Return>', self.OnEnter)
		entry.bind('<KeyPress-KP_Enter>', self.OnEnter)
		entry.focus_set()
		self.entry = entry
		self.sv = sv

	def OnQuit(self, *lArg):
		print "asked to quit, got '{}' as args".format(lArg)
		self.quit()

	def OnEnter(self, *lArg):
		print "Enter happened; got '{}' as args".format(lArg)
		print "  Entry had {}, sv had {}".format(self.entry.get(), self.sv.get())
		self.sv.set('')
		self.labelTime.configure(text=str(int(self.labelTime["text"]) - 1))
		self.labelTotal.configure(text='got something')

def Main():
	"""Main driver for kitten game"""

	app = App()
	app.master.title('Kitten Math')
	app.mainloop()



if __name__ == '__main__':
	Main()

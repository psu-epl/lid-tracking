#Gui application screen for badge scans 
import Tkinter as tk
from time import sleep
from Logging import logger
from datetime import datetime

global root

class NewUserDialog:
	newusercallback = None
	IDNum = None
	top = None
	def __init__(self,parent,newusercallback,IDNum):
		self.newusercallback = newusercallback
		top = self.top =tk.Toplevel(parent)
		top.geometry("{0}x{1}+0+0".format(500, 500))
		tk.Label(top,text='User ID was not found please enter new user details below.').pack()
		if (IDNum == None):
			tk.Label(top,text='Badge Id #').pack()
			self.id = tk.Entry(top)
			self.id.pack(padx=5)
		else:
			self.IDNum = IDNum
			tk.Label(top,text=str(IDNum)).pack()
		tk.Label(top,text='Name:').pack()
		self.name = tk.Entry(top)
		self.name.pack(padx=5)
		tk.Label(top,text='Email:').pack()
		self.email = tk.Entry(top)
		self.email.pack(padx=5)
		tk.Label(top,text='Industry:').pack()
		self.industry = tk.Entry(top)
		self.industry.pack(padx=5)
		tk.Label(top,text='Major:').pack()
		self.major = tk.Entry(top)
		self.major.pack(padx=5)
		self.btnok = tk.Button(top,text='OK',command=self.ok).pack()
	def ok(self):
		try:
			if(self.IDNum ==None):
				self.newusercallback(int(self.id.get()),self.name.get(),self.email.get(),self.industry.get(),0,'user',self.major.get(),'','')
				self.IDNum = int(self.id.get())
			else:
				self.newusercallback(self.IDNum,self.name.get(),self.email.get(),self.industry.get(),0,'user',self.major.get(),'','')
			self.top.destroy()
		except:
			tk.Label(self.top,text='Unable to adduser please check input').pack()
			
class userclockDialog:
	def __init__(self,parent,callback,notes,id,name):
		self.DelNotes = callback
		top = self.top = tk.Toplevel(parent)
		top.geometry("{1}x{1}+0+0".format(500, 500))
		tk.Label(top,text='Notes for %s'%name).pack()
		tk.Label(top,text=notes).pack()
		strtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		tk.Label(top,text='User was logged at %s'%strtime)
		self.top.after(5000,self.top.destroy)
		
		
		
					

class adminDialog:
	def __init__(self,parent,labelcallback):
		self.labelcallback = labelcallback
		top = self.top =tk.Toplevel(parent)
		tk.Label(top, text='Enter Admin Password').pack()
		self.e = tk.Entry(top)
		self.e.pack(padx=5)
		b = tk.Button(top, text='OK', command=self.ok)
		b.pack(pady=5)
	def ok(self):
		print self.e.get()
		self.labelcallback()
			

class FullScreenApp(object):
	newusercallback = None
	delnotecallback = None
	
	def __init__(self, master, **kwargs):
		self.master = master
		self.master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
		self.lblscann = tk.Label(self.master, text='Please scan badge')
		self.lblscann.pack()
		self.b = tk.Button(master,text="New User",command=self.NewUser)
		self.b.place(relx=0,rely=0)
		#self.b = tk.Button(master,text="Admin",command=self.admincallback)
		
		#self.b.pack()
		
		
	# New user button call this will open the dialog for a new user (with a box for id writ in) 
	def NewUser(self):
		global root
		if self.newusercallback == None:
			raise Exception('No callback set')
		dialog = NewUserDialog(root,self.newusercallback,None)
		root.wait_window(dialog.top)
		
	def setnewusercallback(self,callback):
		self.newusercallback = callback
		
	def setdelnotecallback(self,callback):
		self.delnotecallback = callback
		
	
	# unknown user call back reference for main program with id passer
	def getunknownusercallback(self,master):
		self.master = master
		cb = self.Unknownusercallback 
		return cb
		
		
	# get call back for a clock in record
	def getknownusercallback(self,master):
		self.master = master
		cb = self.UserClockRecord
		return cb

	# this function to be called from main program on ID scanned not known 
	def Unknownusercallback(self,_id):
		global root
		if self.newusercallback == None:
			raise Exception('No callback set')
		dialog = NewUserDialog(root,self.newusercallback,_id)
		root.wait_window(dialog.top)

	# this function to be called from main program on user badge scann 
	#self,parent,callback,notes,id,name
	def UserClockRecord(self,notes,id,name):
		sleep(5)
		global root
		if self.delnotecallback ==None:
			raise Exception('No Delnote callback set')
		dialog = userclockDialog(root,self.delnotecallback,notes,id,name)
		root.wait_window(dialog.top)
		




		
	def funccall(self,function):
		function()
		
	def admincallback(self):
		#callback = self.labelcallback
		global root
		#dialog = adminDialog(root,callback)
		#root.wait_window(dialog.top)
		self.lblscann.destroy()
		
	
	def labelcallback(self):
		#sleep(3)
		#print 'calling'
		#tk.Label(self.master, text='something').pack()
		pass
		


			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			



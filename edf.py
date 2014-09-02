
from __future__ import division

import operator

from multiprocessing import Process
from Tkinter import *
import tkMessageBox
import time
from multiprocessing import Process, Queue
import threading
import pygal

def getclocktime():

		clocktimetop=Tk()

		
		
		clockti=StringVar()
		
		def getclockti():
			global clocktime
			
			clocktime=float(clockti.get())
			clocktimetop.destroy()
   		

		Label(clocktimetop, text="SET SCHEDULER CLOCK TIME IN SECONDS:").grid(row=1,column=1)
		Entry(clocktimetop, bd =5,textvariable=clockti).grid(row=1,column=2)

		
		Button(clocktimetop, text ="SUBMIT", command = getclockti).grid(row=4,column=2)
		
		clocktimetop.mainloop()
	#


def giveinput():
		top=Tk()

	#def getinputtk():
		#top=Tk()
		global clocktime
		global processname
		processname=StringVar()
		computationtime=StringVar()
		deadline=StringVar()
		def starttk():
			threading.Thread(target=getresult,).start() 
		def getresult():
			global pn
			pn=processname.get()
			ci=computationtime.get()
			di=deadline.get()
			getinput(pn,ci,di)
   		def showtimer():
			chart()
		def genop():
			createresult()
		Label(top, text="PROCESS NAME:").grid(row=1,column=1)
		Entry(top, bd =5,textvariable=processname).grid(row=1,column=2)

		Label(top, text="ENTER COMPUTATION TIME:").grid(row=2,column=1)
		Entry(top, bd =5,textvariable=computationtime).grid(row=2,column=2)

		Label(top, text="ENTER DEADLINE TIME:").grid(row=3,column=1)
		Entry(top, bd =5,textvariable=deadline).grid(row=3,column=2)
		

		Button(top, text ="SUBMIT", command = starttk).grid(row=4,column=2)
		Button(top, text ="GIVE output",command=showtimer ).grid(row=5,column=1)
		Button(top, text ="Generate Output",command=genop ).grid(row=5,column=2)
		top.mainloop()
	#
	
	
	
	
	
	#top.mainloop()	
def chart():
	gantt=Tk()
	global timer
	length=len(timer)
	for i in range (0,length):
		
		Button(gantt,text= timer[i]).grid(row=1,column=i)
		Label(gantt, text=i).grid(row=2,column=i)
		
	gantt.mainloop()


def timereveal():
	print"revealing timer" 
	global timer
	print timer


def getinput(name,ci,di):	#get from form
	print name +"hello"+ci+di
	global processcounter
	global process
	global semaphore
	
	processcounter += 1
	#print processcounter
	process[processcounter]=process_class()
	process[processcounter].inputcollect(processcounter,name,ci,di)
	arrange(processcounter)
	if(semaphore != 0):	
		switchckeck(processcounter)
	else:
		wait(processcounter)
	

class process_class:    #GET INPUT BY CLASS
	
	
	
	def inputcollect(self,pid,name,ci,di):
		#global entrystack
		print name
		print "Process ID:" + str(pid)
		self.pid=pid
		self.name=name
		self.ai= ci
		self.permaci=ci
		print "ARRIVAL time of process :" + self.name + ": is :"+self.ai
		self.ci= ci
		print "COMPLETION time of process :" + self.name + ": is :"+self.ci
		self.di=di
		print "DEADLINE time of process :" + self.name + ": is :"+self.di
		self.completed=0
		self.waittime=0

	def alterdeadline(self,newdeadline):
		print "altering deadline"
		self.ci=newdeadline
		print self.name +"deadline is"+ str(self.ci)
		printarray()
	def altercomp(self,newci):
		self.completed=newci

def switchckeck(processnum):
	global semaphore
	global contextswitch
	global process
	if (process[processnum].di == process[semaphore].di):
		print "same deadline no switch"
		wait(processnum)
	
	elif (process[processnum].di < process[semaphore].di):
		semaphore=process[processnum].pid
		
		edf_preemit_deadline.pop()
		
		execution()
	else :
		wait(processnum)
	


def wait(processcounter):
	print "entering thread" + str(process[processcounter].pid)
	global semaphore
	print semaphore
	if (semaphore==0):
		var = edf_preemit_deadline.pop()
		print var
		print var[0]
		semaphore =var[0]
		
		execution()
	else:
		while (semaphore!= process[processcounter].pid):
			time.sleep(clocktime)
			process[processcounter].waittime +=1 
		execution()
			
def arrange(processnum):
	global raw_dead_line_queue
	global executionthread	
	global edf_preemit_deadline
	raw_dead_line_queue[processnum]=process[processnum].di
	
	edf_preemit_deadline=sorted(raw_dead_line_queue.iteritems(), key=operator.itemgetter(1),reverse =True)
	print edf_preemit_deadline

def arrangeswitch(processnum,deadline):
	global raw_dead_line_queue
	global executionthread	
	global edf_preemit_deadline
	raw_dead_line_queue[processnum]=deadline
	edf_preemit_deadline=sorted(raw_dead_line_queue.iteritems(), key=operator.itemgetter(1),reverse =True)
	process[processnum].alterdeadline(deadline)
		
		
		
		
def execution():
	global semaphore
	global edf_preemit_deadline
	#print edf_preemit_deadline
	global raw_dead_line_queue
	#print raw_dead_line_queue[semaphore]
	del raw_dead_line_queue[semaphore]
	
	global clocktime
	tempsemaphorevalue=semaphore
	tempci=process[semaphore].ci
	while(tempsemaphorevalue==semaphore and tempci!=0):
		print "entered process name:" + process[semaphore].name 
		time.sleep(clocktime)
		tempci1 = int(tempci) - 1
		tempci=tempci1
	
		print "-------------------"
	
		process[semaphore].completed=int(process[semaphore].permaci)-tempci
		timer.append(process[semaphore].pid)
		print "semaphore value :" + str(semaphore)+"  instance:" +str(tempci)
		#printarray()
		

	if (tempsemaphorevalue!=semaphore and tempci!=0):
		global contextswitch
		print "remaining" +str(tempci)
		arrangeswitch(tempsemaphorevalue,tempci)
		print"context switched"
		#global contextswitch
		#contextswitch=0		
		wait(tempsemaphorevalue)
		

	elif(tempci==0):
		print "executed" + str(process[semaphore].name)
		if not edf_preemit_deadline:
			print edf_preemit_deadline
			print "semaphore to zero"
			semaphore=0
		else:
			var = edf_preemit_deadline.pop()
			semaphore =var[0]
			print "semaphore changed" +str(var[0])
def idle():
	while True:
		
		global semaphore
		global clocktime
		global idletimer	
		while(semaphore==0):
			time.sleep(clocktime)
			idletimer += 1
			timer.append("idle")
def printarray(): #function disabled @ line 222 can enable it to see number of process array
	global processcounter
	global process
	print "printarray"
	if not processcounter:
		print"zero"
		return
	print processcounter
	print"+++++++"
	for i in range(0,processcounter):
		print"process array:"
		print process[i+1].pid
def createresult():
	pie_chart = pygal.Pie()
	bar_chart = pygal.Line()
	pie_chart.title = 'PROCESSOR USAGE WITH EDF SCHEDULING-PREEMITIVE'
	turnaroundchart=pygal.Bar()
	global timer
	global processcounter
	global timer
	global ildetime
	global process
	print timer
	global tempwaittime
	global waitgraph,TAT,CIL,totalci
	waitgraph=list()
	TAT=list()
	CIL=list()
	totalci=0
	global tempwaittime,AWT
	clocks = len(timer)
	tempwaittime=0
	ildetime=timer.count("idle")
	idleprecent=clocks/ildetime
	AWT=0
	pie_chart.add('IDLE', idleprecent)
	print timer
	d = {x:timer.count(x) for x in timer}
	bar_chart.x_labels = map(str, range(1, processcounter))
	turnaroundchart.x_labels = map(str, range(1, processcounter))
	for i in range (0,processcounter):
		#exeprocess=[i+1].pid)
		#print exeprocess
		#print d
		exeprocesscount = d[i+1]
		#print exeprocesscount
		tempwaittime += process[i+1].waittime
		CIL.append(int(process[i+1].ci))
		TAT.append(int(process[i+1].waittime)+int(process[i+1].ci))
		exeprocesspercent=clocks/exeprocesscount
		pie_chart.add(str(i+1), exeprocesspercent)
		waitgraph.append(process[i+1].waittime)
		totalci += int(process[i+1].ci)
		#tempwaittime
	turnaroundchart.add("COMPLETION TIME",CIL)
	turnaroundchart.add("TURN AROUND TIME",TAT)
	bar_chart.add("tasks",waitgraph)
	AWT=tempwaittime/processcounter
	ATT=(tempwaittime+totalci)/processcounter
	turnaroundchart.title="Average turn around time:"+str(ATT)
	bar_chart.title="Average waiting Time :" + str(AWT)
	pie_chart.render_to_file('processorusage.svg')  
	bar_chart.render_to_file('waittime.svg') 	
	turnaroundchart.render_to_file('TAT.svg') 
	

		
	
	
def graph():
	global processcounter
	global process
	global idletimer
	global process
	#bar_chart = pygal.Bar()  
	while True:
		time.sleep(5)
		bar_chart = pygal.Bar()                                        
		#bar_chart.add('IDLE', idletimer) 
		#try:
		for i in range (0,processcounter):
			
			#print process[i+1].pid
			var2 = 1+ process[i+1].completed
			#print var2
			bar_chart.add(str(process[i+1].pid),var2) # Add some values
		#except:
		#	pass		
		bar_chart.render_to_file('runningprocess.svg')  




if __name__ == '__main__':
	counter=0
	idletimer=0
	timer=list()
	semaphore = 0
	processcounter=0
	global process
	processcounter =0
	process={}
	contextswitch=0
	edf_preemit_deadline={}
	clocktime=1
	#getclocktime()  clock time is defaultly set to 1 if you want u can get clock time dynamicalyy with the function enabled
	
	raw_dead_line_queue={}
	threading.Thread(target=graph,).start()
	threading.Thread(target=idle,).start()
	giveinput()
	

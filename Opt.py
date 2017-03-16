import numpy as np
from BellmanFord import BellmanFord
from Dijkstra import Dijkstra
import matplotlib.pyplot as plt
import random as rand
import sys
def Graph(Dur, EdgesFromFinish):
	#Dur= duration of each task
	#EdgesFromFinish= list where each entry the list of nodes dependent on it 
	
	graph=np.zeros((2*len(Dur)+2,2*len(Dur)+2)) 	#graph created, no edges => entry =0

	for i in range(len(Dur)):
		graph[i][i+end+1]+=-Dur[i] 					#Task times added(negative)

	for i in range(len(EdgesFromFinish)):
		for j in EdgesFromFinish[i]:
			graph[i+end+1][j]=-1e-4					#Small negative number for edges with no weight
	
	return graph

def Paths(start, finish, graph):
	#start= vitrual starting node (2*end+1)
	#finish= virtual finishing node (end)
	#graph= graph in the form stated in Graph()

	Paths = []	
	jobsdone=[]
	
	while sum(jobsdone)!=sum(jobs):					#Run loop while some jobs haven't been completed
		Path=BellmanFord(start,finish,graph)		#Find longest (remaining)path 
		Paths.append(Path)							#Save Path
		
		for i in range(len(Path)/2-1):
			
			if Path[2*i+1] not in jobsdone:
				jobsdone.append(Path[2*i+1])		#Add job to jobsdone
		
		graph[Path[-4]][Path[-3]]=0					#remove edge between last and penulimate nodes
	
	return Paths									#List of paths in order of criticality

def Plot(Paths):
	#Takes paths as described in Paths()
	Times=[]										#List of cumulative times for each Path
	tmax=0
	for i in Paths:									#Generating individual cumulative times 
		times=[0]
		t=0
		for j in i:
			if j<end:
				t += Dur[j]
				times.append(t)
		Times.append(times)
		
		if t > tmax:
			tmax=t
	plotted=[]										#List of already plotted nodes
	fig, ax=plt.subplots()							#Create plot
	

	xgrid=[0]
	for i in range(len(Paths)):

		x=(rand.random(),rand.random(),rand.random()) #Randomize colour
		
		for j in range(len(Paths[i])/2-1):			
			if Paths[i][2*j+1] not in plotted:		#Only plot jobs that have not already been plotted
				weight= Times[i][j+1]-Times[i][j]

				l= plt.hlines(Paths[i][2*j+1], float(Times[i][j]), float(Times[i][j+1]), lw=15, color=x)
				plotted.append(Paths[i][(2*j)+1])	#Add job to plotted
				xgrid.append(Times[i][j+1])
	
	print xgrid
	plt.grid(True, linestyle='-.')					

	ygrid = np.arange(0, len(jobs), 1)                                              
	# xgrid = np.arange(0, tmax +1, 25)
	# xgridsmall = np.arange(0, 151, 10)                                               
	ax.set_xticks(xgrid, minor=True)                                                       
	# ax.set_xticks(xgridsmall, minor=True)                                           
	ax.set_yticks(ygrid)                                                       
	plt.show()

######PROBLEM
input = sys.argv[1]
if input == '1':
	Dur=[41,51,50,36,38,45,21,32,32,49,30,19,26] #List of durations for task index number
	
	jobs=range(len(Dur))
	end=jobs[-1]+1
	EdgesFromFinish=[[1,7,10,end],[4,12,end],[3,end],[end],[end],[7,end],[5,9,end],[end],[end],[11,end],[12,end],[end],[end],range(end)]	


######TESTING
#All dependent, 15 tasks
if input == '2':
	Dur=[15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
	jobs=range(len(Dur))
	end=jobs[-1]+1
	EdgesFromFinish=[[1,end],[2,end],[3,end],[4,end],[5,end],[6,end],[7,end],[8,end],[9,end],[10,end],[11,end],[12,end],[13,end], [14,end] ,[end], range(end)]

#Not Dependent, 6 tasks
if input == '3':
	Dur=[1,2,3,4,5,6]
	jobs=range(len(Dur))
	end=jobs[-1]+1
	EdgesFromFinish=[[end],[end],[end],[end],[end],[end],range(end)]

graph=Graph(Dur, EdgesFromFinish)
Paths= Paths(2*end+1,end,graph)
Plot(Paths)
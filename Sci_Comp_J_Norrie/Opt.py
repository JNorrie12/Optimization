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
	
	while len(jobsdone)!=len(jobs):					#Run loop while some jobs haven't been completed
		Path=BellmanFord(start,finish,graph)		#Find longest (remaining)path 
		Paths.append(Path)							#Save Path
		
		for i in range(len(Path)/2-1):
			
			if Path[2*i+1] not in jobsdone:
				jobsdone.append(Path[2*i+1])		#Add job to jobsdone
		
		graph[Path[-2]][Path[-1]]=0
	return Paths									#List of paths in order of criticality

def Time(Dur, Paths):
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
	return Times, tmax

def Plot(Paths, Times, tmax):
	plotted=[]										#List of already plotted nodes
	fig, ax=plt.subplots()							#Create plot
	
	xgrid=[0]
	for i in range(len(Paths)):

		x=(rand.random(),rand.random(),rand.random()) #Randomize colour
		
		for j in range(len(Paths[i])/2-1):			
			if Paths[i][2*j+1] not in plotted:		#Only plot jobs that have not already been plotted
				weight= Times[i][j+1]-Times[i][j]
				
				l= plt.hlines(Paths[i][2*j+1], float(Times[i][j]), float(Times[i][j+1]), lw=15, color=x)
				xgrid.append(Times[i][j+1])

				plotted.append(Paths[i][(2*j)+1])	#Add job to plotted
				
	plt.grid(True, 'both',linestyle='-.')					

	ygrid = np.arange(0, len(jobs), 1)                                              
	xgrid2 = np.arange(0, tmax +1, 25)                                       
	ax.set_xticks(xgrid, minor=True)                                                       
	ax.set_xticks(xgrid2)                                                                                                  
	ax.set_yticks(ygrid)                                                       
	ax.xaxis.grid(True, 'major', linestyle=':', lw=.1)
	plt.xlabel('Time (Minutes)')
	plt.ylabel('Task Number')
	plt.show()

def Bubble(List, List2): #A bubble sort for list of lists, using the first entry of each list as reference
	rearrange=[]
	j=0
	stop=0
	while stop < len(List)/2:
		stop=0
		for i in range(len(List)-1):  
			if i % 2 == j:
				if List[i][1]>List[i+1][1]:
					List[i], List[i+1]=List[i+1], List[i]
					List2[i], List2[i+1]=List2[i+1], List2[i]
				else:
					stop+=1
		j= (j+1 )% 2 
	return List, List2

def PlotSort(Paths, Times, tmax):
	plotted=[]										#List of already plotted nodes
	fig, ax=plt.subplots()							#Create plot
		
	xgrid=[0]
	y=0
	Paths, Times=Bubble(Paths, Times)
	for i in range(len(Paths)):
		if Paths[i][1] not in plotted:
			x=(rand.random(),rand.random(),rand.random()) #Randomize colour
		for j in range(len(Paths[i])/2-1):			
			if Paths[i][2*j+1] not in plotted:		#Only plot jobs that have not already been plotted
				weight= Times[i][j+1]-Times[i][j]

				l= plt.hlines(y, float(Times[i][j]), float(Times[i][j+1]), lw=15, color=x)
				xgrid.append(Times[i][j])
				plt.annotate(str(Paths[i][2*j+1]),(Times[i][j]+weight/2-.4, y-0.015*len(Dur)))
				plotted.append(Paths[i][(2*j)+1])	#Add job to plotted
				y+=1
	plt.grid(True, 'both',linestyle='-.')					
	xgrid2 = np.arange(0, tmax +1, 25)                                       
	ax.set_xticks(xgrid, minor=True)                                                       
	ax.set_xticks(xgrid2)                                                                                                                                                      
	ax.xaxis.grid(True, 'major', linestyle=':', lw=.1)
	plt.xlabel('Time (Minutes)')
	plt.show()

#PROBLEM
input = sys.argv[1]
if input == '1':
	Dur=[41,51,50,36,38,45,21,32,32,49,30,19,26] #List of durations for task index number
	end=len(Dur)
	jobs=range(end)
	EdgesFromFinish=[[1,7,10,end],[4,12,end],[3,end],[end],[end],[7,end],[5,9,end],[end],[end],[11,end],[12,end],[end],[end],range(end)]	

#TESTING
#All dependent, 15 tasks
if input == '2':
	Dur=[15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
	end=len(Dur)
	jobs=range(end)
	EdgesFromFinish=[[end],[0,end],[1,end],[2,end],[3,end],[4,end],\
	[5,end],[6,end],[7,end],[8,end],[9,end],[10,end],[11,end],\
	 [12,end] ,[13,end], range(end)]


#Not Dependent, 6 tasks
if input == '3':
	Dur=[10,20,30,40,50,60]
	end=len(Dur)
	jobs=range(end)
	EdgesFromFinish=[[end],[end],[end],[end],[end],[end],range(end)]

#Simple double dependence, 4 tasks
if input == '4':
	Dur=[15, 30, 27, 15]
	end=len(Dur)
	jobs=range(end)
	EdgesFromFinish=[[3,end],[0,2,end],[3,end],[end],range(end)]


graph=Graph(Dur, EdgesFromFinish)
Paths= Paths(2*end+1,end,graph)
print Paths
Times, tmax=Time(Dur, Paths)
print Times
Plot(Paths, Times, tmax)
PlotSort(Paths, Times, tmax)
print Paths
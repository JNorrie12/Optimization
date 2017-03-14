import numpy as np
from BellmanFord import BellmanFord
from Dijkstra import Dijkstra
import sys
job=range(13)

def Paths(start, finish, graph):
	Path=BellmanFord(start,finish,graph)
	# Path= Dijkstra(27, 13, graph)
	Paths = []
	total=-1
	while total <=-1:
		total=0
		Paths.append(Path) #Append here so we don't get repitition on last
		for i in range(len(Path)-1):
			total+=graph[Path[i]][Path[i+1]]

			if Path[i] >= 14:
				pass
			
			else:
				graph[Path[i]][Path[i]+14]=-1.e-4	
		Path=BellmanFord(start,finish,graph)
		# Path=Dijkstra(27,13,graph)
	return Paths[:-1]

def Bubble(List): #A bubble sort for list of lists, using the first entry of each list as reference
	rearrange=[]
	j=0
	stop=0
	while stop < len(List)/2:
		stop=0
		for i in range(len(List)-1):  
			if i % 2 == j:
				if List[i][0]>List[i+1][0]:
					List[i], List[i+1]=List[i+1], List[i]
				else:
					stop+=1
		j= (j+1 )% 2 
	return List
#Initialising matrix 
inf=sys.maxint

Dur=[41,51,50,36,38,45,21,32,32,49,30,19,26] #List of durations for task index number
EdgesFromFinish=[[1,7,10,13],[4,12,13],[3,13],[13],[13],[7,13],[5,9,13],[13],[13],[11,13],[12,13],[13],[13],[0,1,2,3,4,5,6,7,8,9,10,11,12]]
#All edges from task index number

graph=np.zeros((2*len(Dur)+2,2*len(Dur)+2)) 

for i in range(len(Dur)):
	graph[i][i+14]=-Dur[i] ###Task times added

for i in range(len(EdgesFromFinish)):
	for j in EdgesFromFinish[i]:
		graph[i+14][j]=-1.e-4 #Small negative number to count as negative be not add to weight

Paths= Paths(27,13,graph)

Times=[]
for i in Paths: 
	times=[]
	t=0
	for j in i:
		if j<13:
			t += Dur[j]
			times.append(t)
	Times.append(times)


print Bubble(Times)
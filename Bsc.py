import numpy as np

# edges = {
#     # The edges representing each job
#     "2_start": {"2_finish": 50},
#     "3_start": {"3_finish": 36},
#     "4_start": {"4_finish": 38},

#     # The edges representing dependencies between jobs
#     "2_finish": {"v_finish": 0, "3_start": 0},
#     "3_finish": {"v_finish": 0},
#     "4_finish": {"v_finish": 0}

#     # The edges connecting the virtual start node to every job start
#     "v_start": {
#         "2_start": 0,
#         "3_start": 0,
#         "4_start": 0,
#     },
# }


edges2= {
	
	"v_start": {"1_start":0 ,"2_start":0},#for k not dependent
	
	"1_start": {"1_finish":40},
	"2_start": {"2_finish":36},

	"1_finish": {"v_finish":0},
	"2_finish": {"v_finish":0, "1_start":0}

}

# for i in  edges2['v_start'].values():
	# print i
# print v_start['1_start']
# edges2.get('v_start') same as edges2['v_start']
# print edges2['v_start'].get('1_start')
def connections(v_start):
	return edges2.get(v_start)

def weight(start, finish):
	x=edges2.get(start)
	return x.get(finish)

def LongestPath(edges2, Ppaths):	
	for i in Ppaths:
		# print connections('v_start')
		# print connectio/ns(i)
		for j in connections(i):
			Ppaths.append([i])
		
	print Ppaths

Ppaths=['v_start']
LongestPath(edges2, Ppaths)

def ShortestPath(edges2):
	Ppaths=[] #Initialising start of paths and original weights(0)
	Pweight=[]
	for i in edges2['v_start'].keys():
		Ppaths.append([i]) 
		Pweight.append(edges2['v_start'].get(i))
	
	for i in Ppaths:
		pathend= i[-1]

		if len(edges2[pathend].keys()) ==1:
			i.extend(edges2[pathend].keys()) 
			Pweight.extend(edges2[pathend].values())
		
		if len(edges2[pathend].keys())>1:
			for j in edges2[pathend].keys():
				Ppaths.append([i])
				Ppaths[-1].extend(j)
		for j in edges2[i].keys():
			Ppaths.append([])
	return Ppaths ,Pweight
print ShortestPath(edges2)
# print edges2.values()[0].keys() #Gives you what it is connected to
# print edges2.values()[0].values() #weight of connected edges
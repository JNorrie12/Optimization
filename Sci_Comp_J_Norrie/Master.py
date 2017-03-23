from PIL import Image
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random as rand
import sys
def load_image( infilename) :
	#Creates a greyscale matrix from an image
    
    file = Image.open( infilename )
    bw= file.convert('F')
    data = np.asarray( bw, dtype="float32" )
    return data


def Add_block( array, blockx=(0,0), blocky=(0,0)):
	#Adds block of high energy to  an array.
	#blockx= (column start, column finish)
	#blocky= (row start, row finish)
	
	array.setflags(write=1)
	for i in range(*blocky):
		for j in range(*blockx):
			array[i,j]= 1e6
	return array

def Energy(I, plot=False, block=False): 
	#plot = plots the complexity matrix
	#block = adds areas of high energy to the complextity matrix (Used in report figure 3.6 only)
	Irow=len(I)
	Icol=len(I[0])
	
	C=np.zeros((Irow,Icol))						#Calculate complexity matrix
	for i in range(1,Irow-1):
		for j in range(1,Icol-1):
			C[i][j]=abs(I[i-1][j]-I[i][j])+\
abs(I[i+1][j]-I[i][j])+abs(I[i][j-1]-I[i][j])+abs(I[i][j+1]-I[i][j])
	
			C[0][j]=C[1][j]						#Collumn bundary conditions
			C[-1][j]=C[-2][j]		
	
		C[i][0]=C[i][1]
		C[i][-1]=C[i][-2]
	for j in range(Icol):
		C[0][j]=C[1][j]							#Row boundary conditions
		C[-1][j]=C[-2][j]

	if block:
	 	C=Add_block(C, blockx=(730, 1000), blocky=(100,350) ) #Adding energy blocks
	 	C=Add_block(C, blockx=(0, 370), blocky=(80,350))
	if plot:
		img = Image.fromarray(C)				#Plotting C
		img.show()


	E=np.zeros((Irow,Icol))+C 					#Computing energy matrix E
	for i in range(Irow-1):
	
		for j in range(Icol):
			if j==0:
				E[i+1][j]+=min(E[i][j], E[i][j+1]) #Boundary conditiona
			elif j==Icol-1:
				E[i+1][j]+=min(E[i][j], E[i][j-1])
			else:
				E[i+1][j]+=min(E[i][j-1], E[i][j], E[i][j+1]) #Interior condition
	
	return E

def Seams(E, reversed= False):
	#Calculates seams to remove.
	#reverse changes the argmin so we choose first minimum from the right, 
	#Not used in the final report but an interesting point of experimention. 


	if reversed:
		col=len(E[0])-np.argmin(E[0][::-1])-1 	#Reversed argmin
	
	else:
		col=np.argmin(E[0])						#Normal argmin
	Ppath=[]
	Ppath.append(col)							#Append first column
	print col
	for row in range(len(E)-1): 
		
		if col ==0:
			l=min(E[row+1][col], E[row+1][col+1])	#Boundary conditions
			if l==E[row+1][col]:
				Ppath.append(col)
			else:
				Ppath.append(col+1)
				col += 1
		
		elif col==len(E[0])-1:
			l=min(E[row+1][col], E[row+1][col-1])
			if l==E[row+1][col]:
				Ppath.append(col)
			else:
				Ppath.append(col-1)
				col+=-1

		else:
			l=min(E[row+1][col-1], E[row+1][col], E[row+1][col+1]) #Interior condition
			if l==E[row+1][col]:
				Ppath.append(col)
			elif l==E[row+1][col-1]:
				Ppath.append(col-1)
				col+=-1
			else:
				Ppath.append(col+1)
				col += 1		
		
	return Ppath #List of collumn numbers referring to place at row i

def SeamsBottom(E):             	#Calculating seams from bottom
	
	col=np.argmin(E[-1])			#Finding first minimum value
	Ppath=[]
	Ppath.append(col)				#Append first list coordinate
	print col
	
	for row in range(len(E)-1, 0, -1): 		#Working backwards
		if col ==0:
			l=min(E[row-1][col], E[row-1][col+1]) #Boundery conditons
			if l==E[row-1][col]:
				Ppath.append(col)
			else:
				Ppath.append(col+1)
				col += 1
		
		elif col==len(E[0])-1:
			l=min(E[row-1][col], E[row-1][col-1])
			if l==E[row-1][col]:
				Ppath.append(col)
			else:
				Ppath.append(col-1)
				col+=-1

		else:
			l=min(E[row-1][col-1], E[row-1][col], E[row-1][col+1]) #Interior condition
			if l==E[row-1][col]:
				Ppath.append(col)
			elif l==E[row-1][col-1]:
				Ppath.append(col-1)
				col+=-1
			else:
				Ppath.append(col+1)
				col += 1		
		
	return Ppath[::-1] #Switch path around


def Delete(E, I,Ppath):
	#Deletes paths from two matrices E,I

	for row in range(len(E)):
		del E[row][Ppath[row]] #Deletes the path entry by entry
		del I[row][Ppath[row]]
	
	return E, I

######QUESTIONS#########


input = sys.argv[1]
#Penguin 1, seams chosen from top.
if input == '1':

	I= load_image("penguins.png") #Lodaing image
	
	img= Image.fromarray(I)		#Showing Greyscale
	img.show()
	I=I.tolist()

	for t in range(300):		#300 seams reomoved
		E=Energy(I)
		E=E.tolist()
		
		Ppath=Seams(E)
		
		E, I=Delete(E,I,Ppath) 

#Penguins 2, seams chosen from bottom.
if input == '2':
	I= load_image("penguins.png") #Loading Image
	
	img= Image.fromarray(I)		 #Showing greyscale
	img.show()
	
	I=I.tolist()

	for t in range(300):		#300 seams removed
		E=Energy(I)
		E=E.tolist()
		
		Ppath=SeamsBottom(E)
		
		E, I=Delete(E,I,Ppath) 

#Penguins 3, masking
if input =='4':
	I= load_image("penguins.png")
	E=Energy(I, plot=True)
	
	E=Add_block(E, blockx=(830, 1000), blocky=(599,600) ) #Adding blocks of energy
	E=Add_block(E, blockx=(0, 250), blocky=(599,600))
	
	I=I.tolist()
	E=E.tolist()

	for t in range(300):		#300 seams removed
		Ppath=SeamsBottom(E)
		E, I=Delete(E,I,Ppath) 


I=np.array(I, dtype='float32') #Showing rescaled image
img = Image.fromarray(I)
img.show()
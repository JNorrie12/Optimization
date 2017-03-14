from PIL import Image
import numpy as np
import cv
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import random as rand
# # im=cv.imread("penguins.png")
def load_image( infilename ) :
    input = Image.open( infilename )
    # img=img.load()
    bw= input.convert('F')
    # img= bw.load()
    data = np.asarray( bw, dtype="int32" )
    return data

def average(pixel):
	return (pixel[0]+ pixel[1]+ pixel[2])/3
def path_create(E):
	# print len(E)
	Pvals=np.zeros(len(E[0]))
	Ppaths=[[] for i in range(len(E[0]))] #exclude egdes
	for col in range(1,len(E[0])-1): #ignore edges
		Ppaths[col].append(col)
		for row in range(len(E)-1):	
			# if row==0:
				# Ppaths[col].append(col) #Add starting point of each path
				# Pvals[col]=E[row][col]
			# else:
			l=min(E[row+1][col-1],E[row+1][col],E[row+1][col+1])
			# Pvals[j]+=min(E[i+1][j-1],E[i+1][j],E[i+1][j])
			Pvals[col] +=l
			if l==E[row+1][col]:
				Ppaths[col].append(col)
			elif l==E[row+1][col-1]:
				Ppaths[col].append(col-1)
			else:
				Ppaths[col].append(col+1)
	return Pvals, Ppaths

def Seams(E):
	P=min(E[-1]) #Minimum energy at bottom
	Ppath=[]
	choose=[]
	switch= True
	# for col in range(len(E[0])-1,1, -1): 
		# if E[-1][col]==P and switch==True:
			# switch=False
	col = rand.choice(range(len(E[-1])))
	Ppath.append(col)

	for row in range(len(E)-1,0, -1): #Working backwards
		
		if col ==0:
			l=min(E[row-1][col], E[row-1][col+1])
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
			l=min(E[row-1][col-1], E[row-1][col], E[row-1][col+1])
			if l==E[row-1][col]:
				Ppath.append(col)
			elif l==E[row-1][col-1]:
				Ppath.append(col-1)
				col+=-1
			else:
				Ppath.append(col+1)
				col += 1		
	return Ppath #List of collumn numbers referring to place at row i

def Dreams(E, C,Ppath):
	print len(Ppath)
	for row in range(len(E)):
		del E[row][Ppath[row]]
		del C[row][Ppath[row]]
	return E, C



	# loc is a two-tuple 
	for i in range(len(path)):
		# switch because of array-pixel difference 
		pixels[(path[i],i)] = (255,0,0)
	
	return imgRGB

I= load_image("penguins.png")

Irow=I.shape[0] #i is the number of rows
Icol=I.shape[1] #j in the number of collums

I=np.zeros((Irow,Icol))+I
C=np.zeros((Irow,Icol))
for i in range(1,Irow-1):
	for j in range(1,Icol-1):
		C[i][j]=abs(I[i-1][j]-I[i][j])+abs(I[i+1][j]-I[i][j])+abs(I[i][j-1]-I[i][j])+abs(I[i][j+1]-I[i][j])

	C[i][0]=C[i][1]
	C[i][Icol-1]=C[i][Icol-2]

# img.show()

E=np.zeros((Irow,Icol))+C

# for j in range(Icol):
	# Add[0][j]+=C[0][j]
# print Add[0]
for i in range(Irow-1):
	
	for j in range(Icol):
		if j==0:
			E[i+1][j]+=min(E[i][j], E[i][j+1])
		elif j==Icol-1:
			E[i+1][j]+=min(E[i][j], E[i][j-1])
		else:
			E[i+1][j]+=min(E[i][j-1], E[i][j], E[i][j+1])	
plt.figure(2)
img = Image.fromarray(C)
img.show()
print C
print I
I=I.tolist()
E=E.tolist()

# Pvals, Ppaths =path_create(E)
# for t in range(300):
# 	E, 	C =path_delete(E,C,Pvals,Ppaths)
# 	Pvals, Ppaths =path_create(E) 
# 	print t
def draw_seam(image,path):
	imgRGB = img.convert('RGB')
	pixels = imgRGB.load()

	# loc is a two-tuple 
	for i in range(len(path)):
		# switch because of array-pixel difference 
		pixels[(path[i],i)] = (255,0,0)
	
	return imgRGB

Ppath = Seams(E)
img = Image.open('penguins.png')

for t in range(300):
	E, I=Dreams(E,I,Ppath) 
	Ppath=Seams(E)
	img=draw_seam(img, Ppath)

img.show()
I=np.array(I)
img = Image.fromarray(I)
img.show()
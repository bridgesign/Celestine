import numpy as np
from random import randint

def squared_distance(x,y,w,Il,Ir,d):
	if w==None:
		w = 2*randint(2,5)+1
	distance = 0
	for i in range(-w,w+1):
		for j in range(-w,w+1):
			distance+=((float(Ir[x+d+i][y+j])-float(Il[x+i][y+j]))**2)
	return distance

def abs_difference(x,y,w,Il,Ir,d):
	if w==None:
		w = 2*randint(2,5)+1
	distance = 0
	for i in range(-w,w+1):
		for j in range(-w,w+1):
			distance+=abs(float(Ir[x+d+i][y+j])-float(Il[x+i][y+j]))
	return distance

def zncc(x,y,w,Il,Ir,d):
	if w==None:
		w = 2*randint(2,5)+1
	avgl = 0
	avgr = 0
	for i in range(-w,w+1):
		for j in range(-w,w+1):
			avgl+=float(Il[x+i][y+j])
			avgr+=float(Ir[x+d+i][y+j])
	avgl/=(2*w+1)**2
	avgr/=(2*w+1)**2
	stdl = 0
	stdr = 0

	distance = 0

	for i in range(-w,w+1):
		for j in range(-w,w+1):
			stdl += (float(Il[x+i][y+j])-avgl)**2
			stdr += (float(Ir[x+d+i][y+j])-avgr)**2
			distance += (float(Il[x+i][y+j])-avgl)*(float(Ir[x+d+i][y+j])-avgr)

	stdl/=(2*w+1)**2
	stdr/=(2*w+1)**2
	distance/=(2*w+1)**2
	stdl = stdl**0.5
	stdr = stdr**0.5
	distance/=stdr*stdl
	return distance

def rank_transform(x,y,w,I):
	if w==None:
		w = 2*randint(2,5)+1
	rank = 0
	for i in range(-w,w+1):
		for j in range(-w,w+1):
			if I[x][y]>I[x+i][y+j]:
				rank+=1
	return rank

def census_transform(x,y,w,Il,Ir,d):
	if w==None:
		w = 2*randint(2,5)+1
	distance = 0
	for i in range(-w,w+1):
		for j in range(-w,w+1):
			t = Il[x][y]<Il[x+i][y+j]
			f = Ir[x+d][y]<Ir[x+d+i][y+j]
			if t!=f:
				distance+=1
	return distance
'''In this problem we want to provide a number of rectangles that need to
be packed into the smallest area possible, measured by the (maxX-minX)*(maxY-minY)'''


import random

class Rect:

	def __init__(self,x,y,w,h):
		self.posn = (x,y)
		self.sz = (w,h)

	def getPosn(self):
		'''return a tuple representing the (x,y) coordinate of the UPPER LEFT CORNER'''
		return self.posn

	def getSize(self):
		'''return a tuple representing the (width, height) of the rectangle'''
		return self.sz

	def offset(self,dx,dy):
		(x,y) = self.getPosn()
		self.posn = (x+dx,y+dy)

	def __str__(self):
		posn = self.getPosn()
		if posn is None:
			posn_st = ''
		else:
			posn_st = ':@('+str(posn[0])+','+str(posn[1])+')'
		(w,h) = self.getSize()
		return 'R'+posn_st+':['+str(w)+','+str(h)+']'

	def __repr__(self):
		return self.__str__()

	def area(self):
		(w,h) = self.getSize()
		return w*h
	
	def resetPosn(self):
		self.posn = None


'''let's have a method that splits a big rectangle into a list of rectangles recursively'''
'''Producing a rectangle creates 2 new areas that need to be filled'''
def genRects(width,height,maxWidth,maxHeight):
	if (width < 1 or height < 1):
		return []
	(new_width,new_height) = (random.randint(1,min(width,maxWidth)),random.randint(1,min(height,maxHeight)))

	#all rectangles are at (0,0), the issue will be solved by caller function
	thisRect = Rect(0,0,new_width,new_height)
	myList = [thisRect]

	toRight = genRects(width-new_width,height,maxWidth,maxHeight)
	if (len(toRight) > 0):
		[k.offset(new_width,0) for k in toRight]
		myList.extend(toRight)

	below = genRects(new_width, height-new_height,maxWidth,maxHeight)
	if (len(below) > 0):
		[k.offset(0,new_height) for k in below]
		myList.extend(below)
	return myList

def stripPosns(lst):
	[k.resetPosn() for k in lst]


def main():
	lst = genRects(100,100,20,20)
	stripPosns(lst)
	print(lst)

if __name__ == '__main__':
	main()







import random


'''let's have a method that splits a big rectangle into a list of rectangles recursively'''
def perfectSplit(width,height,maxWidth,maxHeight):
     if (width < 1 or height < 1):
          return []
     (new_width,new_height) = (random.randint(1,min(width,maxWidth)),random.randint(1,min(height,maxHeight)))

     #all rectangles are at (0,0), the issue will be solved by caller function
     thisRect = (new_width,new_height)
     myList = [thisRect]
     toRight = perfectSplit(width-new_width,height,maxWidth,maxHeight)
     if (len(toRight) > 0):
          myList.extend(toRight)

     below = perfectSplit(new_width, height-new_height,maxWidth,maxHeight)
     if (len(below) > 0):
          myList.extend(below)
     return myList

'''randomly produces specified number of rectangles'''
def randomSplit(count, maxWidth, maxHeight):
     lst = []
     for i in range(count):
          lst.append( (random.randint(1,maxWidth), random.randint(1,maxHeight)) )
     return lst

def highVariance(count, maxWidth, maxHeight):
     lst = []
     for i in range(count):

          lst.append( (varianceInt(1,maxWidth), varianceInt(1,maxHeight)) )
     return lst

def varianceInt(lo, hi):
     start = random.randint(lo,hi)
     highest = hi**(hi**.2)
     start = start**(start**.2)
     start = (start - lo)/(highest-lo)
     return start * (hi-lo)































































































































































































































import Driver
import math
import operator

"""
FIND_SOLUTION:
    Define this function in bin_packing.py, along with any auxiliary
functions that you need.  Do not change the Driver.py file at all.
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""

timesRun = 0
bestPlacement = []
avgDimension = 500.5                                        # Please adjust these numbers if dimensions change for max efficiency.

def find_solution(rectangles):
    # print("Number of rectangles:", len(rectangles))
    global timesRun
    placement = [None]*(len(rectangles))                        # Allocate the return list size
    depth = 0
    previousDepth = 0
    breadth = 0
    global avgDimension                                    
    maxBreadth = math.floor((math.sqrt(len(rectangles))*avgDimension))  # The square root of the number of rectangles,
    # print("Expected width of row:", maxBreadth)                         # multiplied by average length of a dimension,
                                                                        # will get our return array close to a square in shape.
    
    sRectangles = sorted(enumerate(rectangles), key=getTupleKey2b, reverse=True)   # Enumerate the original list, then sort by width dimension
    sRectangles = sorted(sRectangles, key=getTupleKey2)                            # Resort by primary key, the height dimension 
    
    for rectangle in sRectangles:
        breadth = breadth + rectangle[1][0]                     # This is distance covered on the x-axis.
        if breadth > maxBreadth:                                # If we have not yet covered our maximum row distance.
            if breadth == rectangle[1][0]:                      # If maximum row distance is less than width of a single box, place it anyway.
                if (previousDepth + rectangle[1][1]) > depth:   
                    depth = previousDepth + rectangle[1][1]     # Set the new maximum depth covered.

            else:                                               # Accomplish all of the aforementioned for the first box in a row.
                breadth = rectangle[1][0]
                previousDepth = depth

        else:                                                   # Accomplish all of the aforementioned, but across the same row.
            if (previousDepth + rectangle[1][1]) > depth:
                depth = previousDepth + rectangle[1][1]

    # print("Original breadth of rows:",maxBreadth)
    # print("Original depth of columns:",depth)
    # print("Original depth / breadth difference:",((depth) / maxBreadth))
    
    newBreadth = (math.floor(((depth) + maxBreadth)/2))      # The average side length of the return box provides the breadth to use in part 2.
    placement = find_better_solution(rectangles, newBreadth)
    return placement

def find_better_solution(rectangles, properBreadth):            # Re-run the original problem, but with a better max breadth in mind. This makes the output more square in shape.
    placement = [None]*(len(rectangles))                        # Allocate the return list size
    global bestPlacement
    global timesRun
    depth = 0
    previousDepth = 0
    breadth = 0                                                         
    maxBreadth = properBreadth
    # print("New expected width of rows:", maxBreadth)
    
    sRectangles = sorted(enumerate(rectangles), key=getTupleKey2b, reverse=True)   # Enumerate the original list, then sort by height dimension
    sRectangles = sorted(sRectangles, key=getTupleKey2)
    
    for rectangle in sRectangles:
        breadth = breadth + rectangle[1][0]                     # This is distance covered on the x-axis.
        if breadth > maxBreadth:                                # If we have not yet covered our maximum row distance.
            if breadth == rectangle[1][0]:                      # If maximum row distance is less than width of a single box, place it anyway.
                if (previousDepth + rectangle[1][1]) > depth:   
                    depth = previousDepth + rectangle[1][1]     # Set the new maximum depth covered.
                coordinate = (0, previousDepth)                 # Set the top left coordinate at the top left of the new row.
                placement[rectangle[0]] = coordinate            # Add the rectangle to the return list.

            else:                                               # Accomplish all of the aforementioned for the first box in a row.
                breadth = rectangle[1][0]
                previousDepth = depth
                coordinate = (0, previousDepth)
                placement[rectangle[0]] = coordinate

        else:                                                   # Accomplish all of the aforementioned, but across the same row.
            if (previousDepth + rectangle[1][1]) > depth:
                depth = previousDepth + rectangle[1][1]
            coordinate = ((breadth - rectangle[1][0]), previousDepth)
            placement[rectangle[0]] = coordinate

    # print("New depth of columns:",depth)
    # print("New depth / breadth difference:",((depth) / maxBreadth))
    # print("Number of coordinates placed:", len(placement),"\n")

    timesRun = timesRun + 1                                                          # Increment loop counter
    
    if (breadth / maxBreadth < .85) or timesRun < 31:                                # Check to see if we're filling out our row
        placement = find_better_solution(rectangles, maxBreadth - (maxBreadth*.005))      # Adjust row size until we do
    else:
        bestPlacement = placement

    # print("\n")
    
    return bestPlacement


def getTupleKey(rectangle):             # Use the height as a key when the list is not enumerated.
    return rectangle[1]

def getTupleKey2(rectangle):            # Use the height as a key when the list is enumerated.
    return rectangle[1][1]

def getTupleKey2b(rectangle):           # Use the width as a key when the list is enumerated.
    return rectangle[1][0]

def getEnumerationKey(rectangle):       # Use the enumeration as a key when the list is enumerated.
    return rectangle[0]

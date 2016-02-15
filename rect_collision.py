import statistics

def get_overlap(sizes, posns):
    global inter_count
    inter_count=0
    if (len(sizes) != len(posns)):
        raise ValueError('Length mismatch.')
    if (len(sizes) == 0):
        return None
    rt = []
    for i in range(len(sizes)):
        rt.append( (posns[i],sizes[i]) )
    
    return grid_detect(rt)

'''
This is a pretty neat rectangle collision detection function.
Note: I did not invent this system or anything. It is a well known technique.
It overlays a grid over the rectangles and checks to see if any cell has more than one rectangle in it.
Then we do the naive overlap check on any rectangles which share a cell.

There are numerous performance gains that could me made, but were entirely unnecessary for this.
'''
def grid_detect(rt):
    avg_w = statistics.median([s[1][0] for s in rt])
    avg_h = statistics.median([s[1][1] for s in rt])
    merp={}
    for r in rt: # n
        coll = place_rect(r,avg_w*3,avg_h*3, merp)
        if coll is not None:
            return coll
    return None

def place_rect(r, dx, dy, merp):
    tx = r[0][0]//dx #initial x
    ty = r[0][1]//dy #initial y
    i = tx
    while i <= r[1][0]//dx: 
        j = ty
        while j <= r[1][1]//dy:
            p = (i,j)
            if (p in merp): #usually this shouldn't get hit, hopefully.
                for t in merp[p]: #for each rect in this cell, compare.
                    if intersecting(r, t):
                        return (r,t)
                merp[p].append(r)
            else:
                merp[p]=[r]
            j += 1
        i += 1
    return None
#ew
inter_count = 0
def intersecting(r1, r2):
    global inter_count
    inter_count+=1
    #print(r1,r2)
    return not(r1[0][0]+r1[1][0] <= r2[0][0] 
        or r1[0][0]+r1[1][0] <= r2[0][0] 
        or r1[0][1]+r1[1][1] >= r2[0][0]
        or r1[0][1]+r1[1][1] >= r2[0][1])
#(0,0,959,-798), (571,0,1204,-116)
r1 = ( (0,0), (959, -798) )
r2 = ( (571, 0), (1204-571, -116))

print(intersecting(r1,r2))


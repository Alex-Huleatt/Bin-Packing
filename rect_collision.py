'''a scaling collision detection system, using 3 strategies.
A divide-and-conquer which can be imagined as a 2D quicksort.
A grid overlay.
The naive n**2.

Takes about ~30 seconds to verify no overlap for 1 million elements.
This would benefit from multithreading in a non-python language
''' 

def get_overlap(sizes, posns):
	if (len(sizes) != len(posns)):
		raise ValueError('Length mismatch')
	if (len(sizes) == 0):
		return None
	rt = []
	for i in range(len(sizes)):
		rt.append( (posns[i],sizes[i]) )
	return grid_detect(rt)

tested = {}
def are_overlapping(p1,s1,p2,s2):
	global tested
	tup = (p1,s1,p2,s2)
	tup2 = (p2,s2,p1,s1)
	if (tup in tested):
		return tested[tup]
	'''returns True if the two specified rectangles are overlapping'''
	ax1,ay1=p1
	bx1,by1=p2
	ax2,ay2=ax1+s1[0],ay1+s1[1]
	bx2,by2=bx1+s2[0],by1+s2[1]
	b = ax1<bx2 and ax2>bx1 and ay1<by2 and ay2>by1
	tested[tup] = b
	tested[tup2] = b
	return b

def naive_detect(rt):
	ret = []
	for i in range(len(rt)):
		for j in range(i+1,len(rt)):
			if are_colliding(rt[i][0],rt[i][1],rt[j][0],rt[j][1]):
				return (rt[i], rt[j])
	return None

#Time for this is n**2 * max_width/dx * max_height/dy
#But this has really good average case
def grid_detect(rt):
	if (len(rt) < 10):
		return naive_detect(rt)
	avg_w= 0
	avg_h= 0
	for r in rt:
		avg_w += r[1][0]
		avg_h += r[1][1]
	avg_w/=len(rt)
	avg_h/=len(rt)
	merp={}
	for r in rt:
		ret = place_rect(r,avg_w*5,avg_h*5, merp)
		if (ret is not None):
			return ret
	return None

def place_rect(r, dx,dy, merp):
	tx = r[0][0]//dx
	ty = r[0][1]//dy
	for i in range(0,int(r[1][0]/dx+1)):
		for j in range(0,int(r[1][1]/dy+1)):
			p = (tx+i,ty+j)
			if (p in merp):
				for t in merp[p]:
					if are_overlapping(r[0],r[1],t[0],t[1]):
						return [(r,t)]
				merp[p].append(r)
			else:
				merp[p]=[r]
	return None




def get_overlap(sizes, posns):
	if (len(sizes) != len(posns)):
		raise ValueError('Length mismatch.')
	if (len(sizes) == 0):
		return None
	rt = []
	for i in range(len(sizes)):
		rt.append( (posns[i],sizes[i]) )
	return grid_detect(rt)

'''
This is a pretty neat rectangle collision detection function I made.
Note: I did not invent this system or anything. It is a well known technique.
It overlays a grid over the rectangles and checks to see if any cell has more than one rectangle in it.
Then we do the naive overlap check on any rectangles which share a cell.

There are numerous performance gains that could me made, but were entirely unnecessary for this.
'''
def grid_detect(rt):
	avg_w,avg_h= 0,0
	for r in rt:
		avg_w += r[1][0]
		avg_h += r[1][1]
	avg_w/=len(rt)
	avg_h/=len(rt)
	merp,rects={},{}
	for r in rt: # n
		place_rect(r,avg_w*3,avg_h*3, merp, rects)
	avg_bucket_len = 0
	for m in rects.keys(): #potentially n
		ax1,ay1=m[0]
		axs,ays=m[1]
		for k in rects[m]: #every *smaller* rectangle nearby, we don't need to compare to larger ones.
			bx1,by1=k[0]
			if (ax1<(bx1+k[1][0]) and (ax1+axs)>bx1 and ay1<(by1+k[1][1]) and (ay1+ays)>by1): 
				return (m,k)
	return None

def place_rect(r, dx,dy, merp, rects):
	tx = r[0][0]//dx
	ty = r[0][1]//dy
	for i in range(int(r[1][0]/dx+1)):
		for j in range(int(r[1][1]/dy+1)):
			p = (tx+i,ty+j)
			if (p in merp): #usually this shouldn't get hit, hopefully.
				ar_r = r[1][0]*r[1][1] #calculate area
				for t in merp[p]:
					if ar_r <= t[1][0]*t[1][1]: #calculate area, only add smaller rectangles.
						if (r in rects):
							rects[r].add(t)
						else:
							rects[r]=set([t])
					else:
						if (t in rects):
							rects[t].add(r)
						else:
							rects[t]=set([r])
			else:
				merp[p]=[r]
	return None
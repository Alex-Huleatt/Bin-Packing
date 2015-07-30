
def get_overlap(sizes, posns):
	if (len(sizes) != len(posns)):
		raise ValueError('Length mismatch.')
	if (len(sizes) == 0):
		return None
	rt = []
	for i in range(len(sizes)):
		rt.append( (posns[i],sizes[i]) )
	return grid_detect(rt)

def are_overlapping(p1,s1,p2,s2):
	'''returns True if the two specified rectangles are overlapping'''
	ax1,ay1=p1
	bx1,by1=p2
	return ax1<(bx1+s2[0]) and (ax1+s1[0])>bx1 and ay1<(by1+s2[1]) and (ay1+s1[1])>by1

def naive_detect(rt):
	ret = []
	for i in range(len(rt)):
		for j in range(i+1,len(rt)):
			if are_overlapping(rt[i][0],rt[i][1],rt[j][0],rt[j][1]):
				return (rt[i], rt[j])
	return None

def grid_detect(rt):
	if (len(rt) < 100): return naive_detect(rt)
	avg_w,avg_h= 0,0
	for r in rt:
		avg_w += r[1][0]
		avg_h += r[1][1]
	avg_w/=len(rt)
	avg_h/=len(rt)
	merp={}
	moar={}
	for r in rt:
		place_rect(r,avg_w*5,avg_h*5, merp, moar)
	avg_bucket_len = 0
	for m in moar.keys():
		ret = naive_detect(merp[m])
		avg_bucket_len+=len(merp[m])
		if (ret is not None):
			return ret
	#print("Average bucket length:",avg_bucket_len/len(moar.keys()))
	return None

def place_rect(r, dx,dy, merp, moar):
	tx = r[0][0]//dx
	ty = r[0][1]//dy
	for i in range(int(r[1][0]/dx+1)):
		for j in range(int(r[1][1]/dy+1)):
			p = (tx+i,ty+j)
			if (p in merp): #usually this shouldn't get hit, hopefully.
				moar[p] = True
				merp[p].append(r)
			else:
				merp[p]=[r]
	return None



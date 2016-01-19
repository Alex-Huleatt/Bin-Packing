
def run(sizes):
	t_x = 0
	res = []
    max_y = 0
    for i in range(0,len(sizes)//2):
        res.append( (t_x,0) )
        t_x+=sizes[i][0]
        max_y = max(sizes[i][1], max_y)
        

	return res
		
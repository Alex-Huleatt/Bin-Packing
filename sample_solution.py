
def find_solution(sizes):
    t_x = 0
    res = []
    for i in range(0,len(sizes)):
        res.append( (t_x,0) )
        t_x+=sizes[i][0]
        

    return res
        
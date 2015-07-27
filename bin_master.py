import sys,importlib,rect_collision,rect_gen,time

def main():

	#number of data sets to use
	max_num = int(sys.argv[1])

	#this dynamically imports the user's module
	lib = importlib.import_module(sys.argv[2])
	results = []
	for i in range(max_num):
		dataset,maxTime = getDataset(i)
		print('Starting set:',i)
		res,time = run(lib, dataset)
		print('Received solution.')
		area = get_area(dataset, res)
		results.append( ('Area:'+str(area), 'Time:'+str(time), 'Valid Solution:'+str(verify(dataset,res))) )
		print(results[-1])


def prof(func):
	def wrapper(*args, **kw):
		startTime = int(round(time.time() * 1000))
		result = func(*args, **kw)
		endTime = int(round(time.time() * 1000))
		elapsed = endTime - startTime
		return (result,elapsed)
	return wrapper

@prof
def run(lib, dataset):
	return lib.run(dataset)

def get_area(sizes, posns):
	min_x, min_y = posns[0]
	max_x, max_y = posns[0]
	for i in range(len(sizes)):
		min_x = min(posns[i][0],min_x)
		min_y = min(posns[i][1],min_y)
		max_x = max(posns[i][0]+sizes[i][0],max_x)
		max_y = max(posns[i][1]+sizes[i][1],max_y)
	return (max_x - min_x) * (max_y - min_y)

def getDataset(num):
	sizes = rect_gen.perfectSplit(1000,1000,20,20)
	maxTime = 100000000.0
	return (sizes,maxTime)

def verify(sizes, posns):
	return rect_collision.get_overlap(sizes,posns) is None



if __name__ == '__main__':
	main()
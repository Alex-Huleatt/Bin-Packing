import sys,importlib,cProfile,rect_collision

def main():

	#number of data sets to use
	max_num = sys.argv[1]

	#this dynamically imports the user's module
	lib = importlib.import_module(sys.argv[2])

	#use cProfile to call func_wrapper
	#Then we can get the time and the area of the user's solution
	#We can add some handy command line tools to let the student's get better profiling

last_area = 0.0
def func_wrapper(lib, dataset):
	global last_area
	last_area = lib.run(dataset)

def getDataset(num):
	return []

def isValid():
	None



if __name__ == '__main__':
	main()
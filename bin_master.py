#!/usr/bin/env python3

import sys,importlib,rect_collision,rect_gen,time,urllib.request,shutil,os
from git import Repo


debug,noprint = False,False

def loadModule(url,sol_name):
	sub = './temp/'
	shutil.rmtree(sub)
	Repo.clone_from(url, sub)
	sys.path.append(sub)
	lib = importlib.import_module(sol_name)
	sys.path.remove(sub)
	return lib

def main():
	global debug
	global noprint
	total_sets = 5
	while 1:
		url = input('url:')
		if(url == '$debug'):
			debug=True
			noprint=False
			continue
		elif(url == '$quit'):
			break
		elif(url == '$noprint'):
			noprint=True
			debug=False
			continue
		else:
			sol_name = input('Solution name:')
			try:
				lib = loadModule(url, sol_name)
				failed,total_area=test_sol(total_sets, lib)
				print(sol_name,'passed',total_sets-failed,'of',total_sets+' sets.','Total area:',total_area)
			except:
				print(sys.exc_info())
				print('Try again.')
			


def test_sol(num_sets, lib):
	if (debug):print('Testing',lib,'on',num_sets,'sets')
	results = []
	keys = ['area','time','valid','passed']
	failed = 0
	inc = num_sets/30
	total_area = 0
	for i in range(num_sets):
		if (i % inc < 1):
			if (not debug and not noprint):
				ct = int(i//inc)
				st = '#'*ct+' '*(30-ct-1)+'|'
				sys.stdout.flush()
				sys.stdout.write('\r'+st)
		dataset,maxTime = getDataset(i)
		res,time = run(lib, dataset)
		area = get_area(dataset, res)

		ver = verify(dataset,res)

		res = dict(zip(keys,(area, time, ver is None, time < maxTime)))
		if (not res['passed'] or not res['valid']):
			failed += 1
		else:
			total_area += area
		results.append(res)
	if(not debug and not noprint):print()
	return failed,total_area

def prof(func):
	def wrapper(*args, **kw):
		startTime = int(round(time.time() * 1000))
		result = func(*args, **kw)
		endTime = int(round(time.time() * 1000))
		elapsed = endTime - startTime
		return (result,elapsed)
	return wrapper

def run(lib, dataset):
	if(debug):print('Running user solution.')
	return prof(lib.run)(dataset)

def get_area(sizes, posns):
	min_x, min_y = posns[0]
	max_x, max_y = posns[0]
	for i in range(len(sizes)):
		min_x,min_y = min(posns[i][0],min_x), min(posns[i][1],min_y)
		max_x, max_y = max(posns[i][0]+sizes[i][0],max_x),max(posns[i][1]+sizes[i][1],max_y)
	return (max_x - min_x) * (max_y - min_y)

def getDataset(num):
	if(debug):print('Getting dataset', num)

	sizes = rect_gen.randomSplit(10000,100,100)
	maxTime = 4
	return (sizes,maxTime)

def verify(sizes, posns):
	if(debug):print('Checking for collisions.')

	collision,time = prof(rect_collision.get_overlap)(sizes,posns)

	if(debug):print('Collision:',(collision,time))
	return collision


if __name__ == '__main__':
	main()
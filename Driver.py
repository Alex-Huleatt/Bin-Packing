
import sys,importlib,rect_collision,rect_gen,time,urllib.request,shutil,os,threading, visualizer



def main():

    default_name = "AlexSolution"
    default_set_count = 10
    benchmark_solution = "sample_solution"
    bench_lib = loadModule(benchmark_solution)

    while (True):
        
        name = input("Module name: ")

        if (len(name)==0):
            name = default_name

        if (name == '$quit'):
            return

        lib = loadModule(name)
        num_sets = input("Number sets: ")

        if (len(num_sets)==0):
            num_sets=default_set_count
        else:
            num_sets = int(num_sets)

        bench_result, sol_result = compare_solutions(bench_lib, lib, num_sets)
        print("Benchmark:",bench_result)
        print(name+":",sol_result)
        print('Ratio:',sol_result['area']/bench_result['area'])

def loadModule(sol_name):
    lib = importlib.import_module(sol_name)
    return lib

def compare_solutions(lib1, lib2, num_sets):
    sets = []
    for i in range(num_sets):

        sets.append(getDataset(i))
    result1=test_sol(sets, lib1)
    result2=test_sol(sets, lib2, visual=True)
    return result1, result2



'''
Creates a new thread so that I can time out the functions
'''
def run_solution(lib, dataset, max_time, visual=False):
    res = {'posns':[], 'passed':False}
    def helper(res):
        res['posns']=lib.run(dataset)
        res['passed']=True
    t = threading.Thread(target=helper,args=(res,))
    t.start()
    t.join(max_time)

    if visual:visualizer.visualize(dataset,res['posns'])

    return res


'''
Given a list of sets and a module, tests all the sets
'''
def test_sol(sets, lib, visual=False):
    failed = 0
    total_area = 0.0
    inc = len(sets)/30
    for i in range(len(sets)):
        sizes = sets[i][0]
        max_time = sets[i][1]

        result = run_solution(lib, sizes, max_time, visual)
        if (result['passed'] and verify(sizes,result['posns'])):
            total_area += get_area(sizes, result['posns'])
            print('Passed:',i)
        else:    
            print('Fail')
            failed += 1

    return {'area':total_area, 'failed':failed}


def get_area(sizes, posns):
    min_x, min_y = posns[0]
    max_x, max_y = posns[0]
    for i in range(len(sizes)):
        min_x,min_y = min(posns[i][0],min_x), min(posns[i][1],min_y)
        max_x, max_y = max(posns[i][0]+sizes[i][0],max_x),max(posns[i][1]+sizes[i][1],max_y)
    return 2*(max_x - min_x) + 2* (max_y - min_y)

def getDataset(num):
    sizes = rect_gen.randomSplit(1000,500,500)
    maxTime = 60
    return (sizes,maxTime)


def verify(sizes, posns):
    collision = rect_collision.get_overlap(sizes,posns)
    if (collision is not None):
        print('Collisions:',collision)
    return collision is None


main()
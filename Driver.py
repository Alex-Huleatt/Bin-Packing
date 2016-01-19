
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
    return test(sets, lib1, lib2, visual=True)



'''
Creates a new thread so that I can time out the functions
'''
def run_solution(lib, dataset, max_time, visual=False):
    res = {'posns':[], 'passed':False}
    def helper(res):
        res['posns']=lib.find_solution(dataset)
        res['passed']=True
    t = threading.Thread(target=helper,args=(res,))
    t.start()
    t.join(max_time)

    #if visual:visualizer.visualize(dataset,res['posns'])

    return res

def run_set(lib1, lib2, dataset, visual=False):
    sizes =dataset[0]
    max_time = dataset[1]

    result1 = run_solution(lib1, sizes, max_time, visual)
    result2 = run_solution(lib2, sizes, max_time, visual)
    return result1,result2



'''
Given a list of sets and a module, tests all the sets
'''
def test(sets, lib1, lib2, visual=False):
    failed = 0
    total_area = 0.0
    inc = len(sets)/30
    lib1_results = {"area":0.0,"failed":0}
    lib2_results = {"area":0.0,"failed":0}

    for i in range(len(sets)):
        l1_passed = False
        l2_passed = False
        l1_ar = 0.0
        l2_ar = 0.0
        result1, result2 = run_set(lib1, lib2, sets[i], visual)
        if (result1['passed'] and verify(sets[i][0],result1['posns'])):
            l1_ar=get_area(sets[i][0], result1['posns'])
            lib1_results['area']+=l1_ar
            l1_passed=True
        else:    
            lib2_results['failed']+=1

        if (result2['passed'] and verify(sets[i][0],result2['posns'])):
            l2_ar=get_area(sets[i][0], result2['posns'])
            lib2_results['area']+=l2_ar
            l2_passed=True
        else:    
            lib2_results['failed']+=1


        if (l1_passed and l2_passed):
            print("Both passed set",i, 'L1:',l1_ar,'L2:',str(l2_ar)+".",'% improvement',str(100*(1 - l2_ar/l1_ar)))

    return (lib1_results,lib2_results)


def get_area(sizes, posns):
    min_x, min_y = posns[0]
    max_x, max_y = posns[0]
    for i in range(len(sizes)):
        min_x,min_y = min(posns[i][0],min_x), min(posns[i][1],min_y)
        max_x, max_y = max(posns[i][0]+sizes[i][0],max_x),max(posns[i][1]+sizes[i][1],max_y)
    return 2*((max_x - min_x) + (max_y - min_y))

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
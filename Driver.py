
import sys,importlib,rect_collision,rect_gen,time,urllib.request,shutil,os,threading,random

try:
    import visualizer
    can_visualize=True
except ImportError:
    can_visualize=False


def main():
    global can_visualize
    module1_name_default = "bin_packing"
    module2_name_default = "naive_solution"
    default_set_count = 10

    while (True):
        
        name = input("Module 1 name (default: "+module1_name_default+"): ")

        if (len(name)==0):
            name = module1_name_default

        if (name == '$quit'):
            return

        lib1 = load_module(name)
        name = input("Module 2 name (default: "+module2_name_default+"): ")

        if (len(name)==0):
            name = module2_name_default

        
        lib2 = load_module(name)
        num_sets = input("Number sets(default: "+str(default_set_count)+"): ")

        if (len(num_sets)==0):
            num_sets=default_set_count
        else:
            num_sets = int(num_sets)
        visual=False
        if (can_visualize):
            while (True):
                visual = input("Visualize? y/n: ")
                if (visual == 'y'):
                    visual = True
                    break
                elif (visual=='n'):
                    visual = False
                    break
                else:
                    print("That was not y or n, try again.")


        lib1_result, lib2_result = compare_solutions(lib1, lib2, num_sets, visual=visual)
        print("Module 1:",lib1_result)
        print("Module 2:",lib2_result)
        print('Average ratio:',lib1_result['area']/lib2_result['area'])

def load_module(sol_name):
    lib = importlib.import_module(sol_name)
    return lib

def compare_solutions(lib1, lib2, num_sets, visual=False):
    sets = []
    for i in range(num_sets):
        sets.append(get_dataset(i))
    return test(sets, lib1, lib2, visual)



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

    if visual:visualizer.visualize(dataset,res['posns'])

    return res

def run_set(lib1, lib2, dataset, visual=False):
    sizes =dataset[0]
    max_time = dataset[1]

    result1 = run_solution(lib1, sizes, max_time, visual)
    result2 = run_solution(lib2, sizes, max_time, visual)
    return result1,result2



'''
Given a list of sets and two modules, tests all the sets
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
            print("Both passed set",i, 'L1:',l1_ar,'L2:',str(l2_ar)+".",'% improvement',str(100*(1 - l1_ar/l2_ar)))
        else:
            print("Module 1 passed:",l1_passed,", Module 2 passed:", l2_passed)

    return (lib1_results,lib2_results)


def get_area(sizes, posns):
    min_x, min_y = posns[0]
    max_x, max_y = posns[0]
    for i in range(len(sizes)):
        min_x,min_y = min(posns[i][0],min_x), min(posns[i][1],min_y)
        max_x, max_y = max(posns[i][0]+sizes[i][0],max_x),max(posns[i][1]+sizes[i][1],max_y)
    return 2*((max_x - min_x) + (max_y - min_y))

def get_dataset(num):
     #generate (1000,10000) rectangles
     #widths in the range [1,1000]
     #heights in the range [1,1000]
    numRectangles = random.randint(1000,10000)
    sizes = rect_gen.randomSplit(numRectangles,1000,1000)
    maxTime = 60
    return (sizes,maxTime)


def verify(sizes, posns):
    collision = rect_collision.get_overlap(sizes,posns)
    if (collision is not None):
        print('Collisions:',collision)
    return collision is None


main()

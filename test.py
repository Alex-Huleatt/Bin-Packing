

@profile
def expensive_function():
	lst = []
	for j in range(100000):
		for k in range(10):
			lst.append(j)



expensive_function()



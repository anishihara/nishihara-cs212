"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes. OK
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky. OK
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon. OK
7. The person who arrived on Thursday is not the designer. OK
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

def day_after(a,b):
	if b+1 == a:
		return True
	return False

def solve_puzzle():
    days = Monday, Tuesday, Wednesday, Thursday, Friday = [0,1,2,3,4]
    orderings = list(itertools.permutations(days))
    return next([Hamming,Knuth,Minsky,Simon,Wilkes]
    	for [Hamming,Knuth,Minsky,Simon,Wilkes] in orderings
    	if day_after(Knuth,Simon)
    	for [programmer, writer, manager, designer, _] in orderings
    	if programmer != Wilkes
    	and writer != Minsky
    	and Thursday != designer
    	and day_after(Knuth,manager)
    	for [tablet, laptop, droid, iphone, _] in orderings
    	if Wednesday == laptop
    	if (programmer == Wilkes and droid == Hamming) or (programmer == Hamming and droid == Wilkes)
    	if manager != Knuth and manager != tablet
    	and Friday != tablet
    	and designer != droid
    	and ((laptop == Monday and Wilkes == writer) or (laptop == writer and Wilkes == Monday))
    	and ((iphone == Tuesday) or (tablet == Tuesday))
    	)

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    solve_result = solve_puzzle()
    people = ['Hamming','Knuth','Minsky','Simon','Wilkes']
    result = range(5)
    count = 0
    for i in solve_result:
    	result[i]=people[count]
    	count+=1
    return result

print logic_puzzle()
    

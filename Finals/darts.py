# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""


def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    # your code here
    #preparing scores list
    scores = []
    double_scores = []
    for i in range(1,21):
        scores.append(i)
        scores.append(i*2)
        double_scores.append(i*2)
        scores.append(i*3)
    scores.append(25)
    scores.append(50)
    double_scores.append(50)
    scores.sort(reverse=True)
    scores = [0] + scores
    result_scores = []
    for dart1 in scores:
        for dart2 in scores:
            left = total - dart1 - dart2
            if left == 0:
                if dart2 in double_scores:
                    return [name(dart1),name(dart2)]
            if left in double_scores:
                if dart1 == 0: result_scores = [name(dart2),name(left,last_dart=True)]
                elif dart2 == 0: result_scores = [name(dart1),name(left,last_dart=True)]
                else: result_scores = [name(dart1),name(dart2),name(left,last_dart=True)]
                return result_scores
    return None
                
def name(d, last_dart=False):
    single_scores = []
    double_scores = []
    triple_scores = []
    if d == 0:
        return None
    if d == 25:
        return 'SB'
    if d == 50:
        return 'DB'
    for i in range(1,21):
        single_scores.append(i)
        double_scores.append(i*2)
        triple_scores.append(i*3)
    if last_dart:
        if d in double_scores:
            return 'D' + str(d/2)
        if d in single_scores:
            return 'S' + str(d)
        if d in triple_scores:
            return 'T' + str(d/3)
    else:
        if d in single_scores:
            return 'S' + str(d)
        if d in double_scores:
            return 'D' + str(d/2)
        if d in triple_scores:
            return 'T' + str(d/3)
    return None
    
test_darts()     

"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""


def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    #your code here
    result = {}
    for ring in ring_outcome(target,miss):
        for section in section_outcome(target,miss):
            if target != 'SB' and target != 'DB':
                if ring[0] != 'OFF':
                    result[ring[0]+section[0]] = ring[1]*section[1]
                else:
                    result['OFF'] = ring[1]*section[1]
            else:
                if section[0]=='B':
                    if ring[0] == 'SB':
                        result['SB'] = ring[1]*section[1]
                    elif ring[0] == 'DB':
                        result['DB'] = ring[1]*section[1]
                    else:
                        for i in range(1,21):
                            result['S'+str(i)] += ring[1]*section[1]/20
                else:
                    if ring[0] != 'SB' and ring[0] != 'DB':
                        result[ring[0]+section[0]] = section[1]
                    
    return result
    
def ring_outcome(target,miss):
    result = []
    #identify the ring
    ring = target[0]
    section = target[1:]
    # miss for the rings
    if section != 'B':
        if ring == 'T':
            result.append(('S',miss))
        elif ring == 'D':
            result.append(('S',miss/2))
            result.append(('OFF',miss/2))
        elif ring == 'S':
            new_miss = miss/5
            result.append(('D',new_miss/2))
            result.append(('T',new_miss/2))
    else:
        if ring == 'S':
            result.append(('DB',miss/4))
            result.append(('S',miss*3/4))
        elif ring == 'D':
            new_miss = 3*miss
            result.append(('S',new_miss*2/3))
            result.append(('SB',new_miss/3))
    probability = lambda x: x[1]
    total_probability = 0.
    for ring_result in result:
        total_probability += probability(ring_result)
    if target != 'SB' and target != 'DB':
        result.append((ring, 1. - total_probability))
    else:
        result.append((target, 1. - total_probability))
    return result
            
def section_outcome(target,miss):
    result = []
    section = target[1:]
    sections = [20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5]
    if target != 'SB' and target != 'DB':
        index = sections.index(int(section))
        next_index = (index + 1)%len(sections)
        previous_index = (index - 1)%len(sections)
        result.append((str(sections[next_index]),miss/2))
        result.append((str(sections[previous_index]),miss/2))
    else:
        for i in sections:
            result.append((str(i),miss/20))
    probability = lambda x: x[1]
    total_probability = 0.
    for section_result in result:
        total_probability += probability(section_result)
    result.append((section , 1. - total_probability))
    return result
    

def best_target(miss):
    "Return the target that maximizes the expected score."
    #your code here
    sections = [20,1,18,4,13,6,10,15,2,17,3,19,7,10,8,11,14,9,12,5]
    scores = []
    for i in range(1,21):
        scores.append(i)
        scores.append(i*2)
        scores.append(i*3)
    scores.append(25)
    scores.append(50)
    best_target = ''
    maximum = 0.
    for i in scores:
        target = name(i)
        if target != None:
            max_target = 0
            target_outcome = outcome(target,miss)
            for key in target_outcome:
                max_target += target_outcome[key]*score(key)
            if max_target>maximum:
                best_target = target
                maximum = max_target
    return best_target
    
def score(d):
    if d == 'OFF':
        return 0
    if d == 'SB':
        return 25
    if d == 'DB':
        return 50
    ring = d[0]
    section = int(d[1:])
    if ring == 'T':
        return 3*section
    if ring == 'D':
        return 2*section
    if ring == 'S':
        return section
    return None
    
def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))


test_darts2()
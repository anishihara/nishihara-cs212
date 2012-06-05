"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.

"""

def bowling(balls):
    "Compute the total score for a player's game of bowling."
    ## bowling([int, ...]) -> int
    ## your code here
    scores = []
    frames = []
    while balls:
        ball = balls.pop(0)
        if ball == 10 and len(frames) != 9:
            frames.append({'f_pin':10,'s_pin':0,'t_pin':0})
        else:
            if len(frames) == 9:
                second_ball = balls.pop(0)
                if ball == 10 or second_ball == 10 or ball+second_ball == 10:
                    third_ball = balls.pop(0)
                    frames.append({'f_pin':ball,'s_pin':second_ball,'t_pin':third_ball})
                else:
                    frames.append({'f_pin':ball,'s_pin':second_ball,'t_pin':0})
            else:
                second_ball = balls.pop(0)
                frames.append({'f_pin':ball,'s_pin':second_ball,'t_pin':0})

    for i in range(len(frames)):
        frame = frames[i]
        if i == 9:
            scores.append(frame['f_pin'] + frame['s_pin'] + frame['t_pin'])
        else:
            #strike
            if frame['f_pin'] == 10:
                next_frame = frames[i+1]
                next_t_ball = next_frame['f_pin']
                if next_t_ball == 10:
                    if i <= 7:
                        next_t_ball = next_t_ball + frames[i+2]['f_pin']
                    else:
                        next_t_ball = next_t_ball + next_frame['s_pin']
                else:
                    next_t_ball = next_t_ball + next_frame['s_pin']
                scores.append(10+next_t_ball)
            #spare
            elif frame['f_pin']+frame['s_pin'] == 10:
                next_frame = frames[i+1]
                scores.append(10+next_frame['f_pin'])
            else:
                scores.append(frame['f_pin'] + frame['s_pin'] + frame['t_pin'])
    return sum(scores)




def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])


test_bowling()
#print bowling([10, 5,5] * 5 + [10])
   
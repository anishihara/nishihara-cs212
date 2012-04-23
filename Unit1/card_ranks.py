# -----------
# User Instructions
# 
# Modify the card_ranks() function so that cards with
# rank of ten, jack, queen, king, or ace (T, J, Q, K, A)
# are handled correctly. Do this by mapping 'T' to 10, 
# 'J' to 11, etc...

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = [r for r,s in cards]
    changed_ranks = []
    for rank in ranks:
        if rank == 'T':
            changed_ranks.append(10)
        elif rank == 'J':
            changed_ranks.append(11)
        elif rank == 'Q':
            changed_ranks.append(12)
        elif rank == 'K':
            changed_ranks.append(13)
        elif rank == 'A':
            changed_ranks.append(14)
        else:
            changed_ranks.append(int(rank))
    ranks = changed_ranks 
    ranks.sort(reverse=True)
    return ranks

def card_ranks2(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA)'.index(r) for r,s in cards]
    ranks.sort(reverse=True)
    return ranks

print card_ranks(['AC', '3D', '4S', 'KH']) #should output [14, 13, 4, 3]
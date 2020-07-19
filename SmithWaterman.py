from __future__ import division, print_function
import numpy as np

pt ={'match': 1, 'mismatch': -3, 'gap': -3}


def pre_su(s1_len, s2_len, i, j, max_i, max_j):
    
    """ return prefix = true if seq2 is the prefix of seq1 """
    try:
        
        s1_end = s1_len - max_i
        s2_end = s2_len - max_j
        
        # Case 1: i = j = 0
        if i == 0 and j == 0 and s1_len>s2_len:
            return True

        if i == 0 and j == 0 and s2_len>s1_len:
            return False

        # Case 2: Compare both start and end of seq

        if i < j and s1_end >= s2_end:
            return True

        if i > j and s2_end > s1_end:
            return False

        # Case 3: Compare both end and longer seq

        if i < j and s1_end < s2_end:

            if j < s2_end:
                return False
            else:
                return True

        if i > j and s1_end >= s2_end:

            if i <= s1_end:
                return True
            else:
                return False

    except:
        print("Undefined. Please check for error")

def mch(l1, l2):
    
    """ find if both letter are match, gap or mismatch """
    if l1 == l2:
        return pt['match']
    elif l1 == '-' or l2 == '-':
        return pt['gap']
    else:
        return pt['mismatch']

def smith_waterman(s1, s2):
    """ return the score for the local alignment of two sequences, whether the sequence is prefix or suffix and 
    the starting point of overlap

    The score will be set to 0 when either one is a contained read
    """

    m, n = len(s1), len(s2)  #len of two sequences
    H = np.zeros((m+1, n+1)) #initialise matrices, H (for scoring) and T (for indicating path-backtrack)
    T = np.zeros((m+1, n+1))
    max_score = 0

    # Score, Pointer Matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sc_diag = H[i-1][j-1] + mch(s1[i-1], s2[j-1])
            sc_up = H[i][j-1] + pt['gap']
            sc_left = H[i-1][j] + pt['gap']
            H[i][j] = max(0,sc_left, sc_up, sc_diag)
            if H[i][j] == 0: T[i][j] = 0
            if H[i][j] == sc_left: T[i][j] = 1
            if H[i][j] == sc_up: T[i][j] = 2
            if H[i][j] == sc_diag: T[i][j] = 3
            if H[i][j] >= max_score: # to store the best score
                max_i = i
                max_j = j
                max_score = H[i][j];

    align1, align2 = '', ''
    i,j = max_i,max_j

    #Traceback from max score
    while T[i][j] != 0:
        if T[i][j] == 3: #diagonal: see above
            a1 = s1[i-1]
            a2 = s2[j-1]
            i -= 1
            j -= 1
        elif T[i][j] == 2: #up_gap
            a1 = '-'
            a2 = s2[j-1]
            j -= 1
        elif T[i][j] == 1: #left_gap
            a1 = s1[i-1]
            a2 = '-'
            i -= 1
        align1 += a1
        align2 += a2

    # reverse the alignment
    align1 = align1[::-1]
    align2 = align2[::-1]
    sym = ''
    iden = 0
    overlap_score = 0

    for k in range(len(align1)):
        a1 = align1[k]
        a2 = align2[k]
        if a1 == a2:      #match       
            sym += a1
            iden += 1
            overlap_score += pt['match']
        elif a1 != a2 and a1 != '-' and a2 != '-': #Mismatch and not gap
            sym += ' '
            overlap_score += pt['mismatch']

        elif a1 == '-' or a2 == '-':               #either one is gap
            sym += '_'
            overlap_score += pt['gap']



    identity = iden / min(len(s1), len(s2)) * 100

    # if it is a contained read of first seq
    if (identity == 100 and (i != 0 and max_i != len(s1))):
        max_score = 0
    # if it is a contained read of second seq
    if (identity == 100 and (j != 0 and max_j != len(s2))):
        max_score = 0
    # if they are the same 
    if (identity == 100 and len(s1) == len(s2)):
        max_score = 0        
    # if they start from the first position
    if (identity == 100 and i == 0 and j == 0):
        max_score = 0
    # if they ends at the last position
    if (identity == 100 and max_i == len(s1) and max_j == len(s2)):
        max_score = 0

    print("overlap score =", overlap_score)
#     print("max score=", max_score)
#     print("sym= " + sym)

    # find out whether the seq2 is prefix or suffix of seq1
    prefix = pre_su(len(s1), len(s2), i, j, max_i, max_j)

#     if(prefix):
#         print("prefix= ", s2)
#         print("suffix= ", s1)

#     else:
#         print("prefix= ", s1)
#         print("suffix= ", s2)

#     print("i= ", i)
#     print("max_i= ", max_i)

#     print("j= ", j)
#     print("max_j= ", max_j)

#     print("len(s1)= ", len(s1))
#     print("len(s2)= ", len(s2))

    return max_score, prefix, i, max_i, j, max_j
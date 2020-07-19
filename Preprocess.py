from itertools import groupby


def fasta_iter(fasta_name):
    
    """ read from fasta file """

    # open the fasta file
    fh = open(fasta_name)

    # ditch the boolean (x[0]) and just keep the header or sequence since
    # we know they alternate.
    faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))

    for header in faiter:
        # drop the ">", remove whitespace
        headerStr = header.__next__()[1:].strip()

        # join all sequence lines to one.
        seq = "".join(s.strip() for s in faiter.__next__())
        
        yield(seq)

                           
                  
def distance_comparator(seq1, seq2):
    
    """ parallel distance k-mer computation, return true if the distance smaller than the threshold 0.3 """
         
    count = 0
    i = 0
    j = 0
    k = 9 #9-mer
    
    while (i < len(seq1) - k + 1) and (j < len(seq2) - k + 1):
        
        if seq1[i] < seq2[j]: 
            i += 1
        elif seq1[i] > seq2[j]:
            j += 1
           
        else:
            count += 1
            i += 1
            j += 1
            
    distance = 1 - count/ (min(len(seq1), len(seq2)) - k + 1)
                           
    if distance < 0.3:
        return True
                           
    return False
    
def filter_seq(seq_list):
    
    """ return a list of read with their can-be-compared item 
        {seq1: [seq2, seq3], seq2: [seq1, seq3], seq3: [seq1, seq2]} 
    """

    processed = {}
    m = 0
    for i in seq_list:
        
        processed[seq_list[i]] = []
        n = 0
        for j in seq_list:
               
            if n > m:
                 if distance_comparator(i, j):
                        processed[seq_list[i]].append(seq_list[j])                        
            n += 1                       
        m += 1
    
    return processed
                              
def preprocess(fasta_name):
    """ sort the sequence into lexicographical order, store the sorted_seq:seq as key value pair """
    
    sequence_list = {}
    
    gen = fasta_iter(fasta_name)
    
    for seq in gen:
        # tim sort O(n log n)
        sorted_seq = ''.join(sorted(seq))
        sequence_list[sorted_seq] = seq
                      
    processed = filter_seq(sequence_list)
    
    
    return processed

                           
        
                           
                        
                      
    
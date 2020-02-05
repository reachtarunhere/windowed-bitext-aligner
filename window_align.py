def CandidateGenerator(trg_max, window_size=5):
    """ trg_max is len of trg sentences file"""

    half_margin = window_size//2
    
    def gen_candidate(i):
        def valid_trg(x): return 0<=x<trg_max
        
        return [x for x in range(i-half_margin, i+half_margin+1) if valid_trg(x)]

    return gen_candidate



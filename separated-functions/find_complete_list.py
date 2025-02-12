import numpy as np

def find_complete_list(pair_list,song_length):
    """
    Finds all smaller diagonals (and the associated pairs of repeats) 
    that are contained in pair_list, which is composed of larger 
    diagonals found in find_initial_repeats.
        
    Args
    ----
    pair_list: np.array
        list of pairs of repeats found in earlier step
        (bandwidths MUST be in ascending order). If you have
        run find_initial_repeats before this script,
        then pair_list will be ordered correctly. 
           
    song_length: int
        song length, which is the number of audio shingles.
   
    Returns
    -------  
    lst_out: np.array 
        list of pairs of repeats with smaller repeats added
    """
    # Find the list of unique repeat lengths
    bw_found = np.unique(pair_list[:,4])
    bw_num = np.size(bw_found, axis=0)
    
    # If the longest bandwidth is the length of the song, then remove that row
    if song_length == bw_found[bw_num-1]: 
        pair_list[-1,:] = []
        bw_found[-1] = []
        bw_num = (bw_num - 1)
        
    # Initalize temp variables
    p = np.size(pair_list,axis=0)
    add_mat = []

    # Step 1: For each found bandwidth, search upwards (i.e. search the larger 
    #        bandwidths) and add all found diagonals to the variable add_mat        
    for j in range (1,bw_num+1):
        band_width = bw_found[j-1]
        
        # Isolate pairs of repeats that are length bandwidth
        bsnds = np.amin((pair_list[:,4] == band_width).nonzero()) # Return the minimum of the array
        bends = (pair_list[:,4] > band_width).nonzero()
    
        # Convert bends into an array
        bend = np.array(bends)
    
        if bend.size > 0:
            bend = np.amin(bend)
        else:
            bend = p
    
        # Part A1: Isolate all starting time steps of the repeats of length bandwidth
        start_I = pair_list[bsnds:bend, 0]
        start_J = pair_list[bsnds:bend, 2]
        combine_starts = [start_I,start_J]
        
        all_vec_snds = np.concatenate(combine_starts)
        int_snds = np.unique(all_vec_snds)
    
        # Part A2: Isolate all ending time steps of the repeats of length bandwidth
        end_I = pair_list[bsnds:bend, 1] # Similar to definition for SI
        end_J = pair_list[bsnds:bend, 3] # Similar to definition for SJ
        combine_ends = [end_I,end_J]
        
        all_vec_ends = np.concatenate(combine_ends)
        int_ends = np.unique(all_vec_ends)
    
        # Part B: Use the current diagonal information to search for diagonals 
        #       of length BW contained in larger diagonals and thus were not
        #       detected because they were contained in larger diagonals that
        #       were removed by our method of eliminating diagonals in
        #       descending order by size
        add_srows = find_add_srows_both_check_no_anno(pair_list, int_snds, band_width)
        add_erows = find_add_mrows_both_check_no_anno(pair_list, int_snds, band_width)
        add_mrows = find_add_erows_both_check_no_anno(pair_list, int_ends, band_width)
        
        # Check if any of the arrays are empty, if so, reshape them
        if add_mrows.size == 0:
            column = add_srows.shape[1]
            add_mrows = np.array([],dtype=np.int64).reshape(0,column) 
        elif add_srows.size == 0:
            column = add_erows.shape[1]
            add_mrows = np.array([],dtype=np.int64).reshape(0,column) 
        elif add_erows.size == 0:
            column = add_srows.shape[1]
            add_mrows = np.array([],dtype=np.int64).reshape(0,column) 
       
        # Add the new pairs of repeats to the temporary list add_mat
        add_mat.extend((add_srows,add_erows,add_mrows))
        new_mat = np.concatenate(add_mat)
      
    # Step 2: Combine pair_list and new_mat. Make sure that you don't have any
    #         double rows in add_mat. Then find the new list of found 
    #         bandwidths in combine_mat.
    combo = [pair_list,new_mat]
    combine_mat = np.concatenate(combo)

    combine_mat = np.unique(combine_mat,axis=0)
    combine_inds = np.argsort(combine_mat[:,4]) # Return the indices that would sort combine_mat's fourth column
    combine_mat = combine_mat[combine_inds,:]
    c = np.size(combine_mat,axis=0)
    
    # Again, find the list of unique repeat lengths
    new_bw_found = np.unique(combine_mat[:,4])
    new_bw_num = np.size(new_bfound,axis=0)
    full_lst = []
    
    # Step 3: Loop over the new list of found bandwidths to add the annotation
    #         markers to each found pair of repeats
    for j in range(1,new_bw_num+1):
        new_bw = new_bw_found[j-1]
        # Isolate pairs of repeats in combine_mat that are length bandwidth
        new_bsnds = np.amin((combine_mat[:,4] == new_bw).nonzero()) # Return the minimum of the array
        new_bends = (combine_mat[:,4] > new_bw).nonzero() 

        # Convert new_bends into an array
        new_bend = np.array(new_bends)
    
        if new_bend.size > 0:
            new_bend = np.amin(new_bend)
        else:
            new_bend = c
        
        band_width_mat = np.array((combine_mat[new_bsnds:new_bend,]))
        length_band_width_mat = np.size(band_width_mat,axis=0)

        temp_anno_lst = np.concatenate((band_width_mat,(np.zeros((length_band_width_mat,1)))),axis=1).astype(int)

        # Part C: Get annotation markers for this bandwidth
        temp_anno_lst = add_annotations(temp_anno_lst, song_length)
        full_lst.append(temp_anno_lst)
        final_lst = np.vstack(full_lst)
    
    lst_out = final_lst
    
    return lst_out

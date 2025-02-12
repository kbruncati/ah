#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search.py 

This file contains the following functions:
    
    * find_add_erows - Finds pairs of repeated structures, represented as 
    diagonals of a certain length, k, that end at the same time step as 
    previously found pairs of repeated structures of the same length.

    * find_add_mrows - Finds pairs of repeated structures, represented as 
    diagonals of a certain length, k, that neither start nor end at the same 
    time steps as previously found pairs of repeated structures of the same 
    length. 
    
    * find_add_srows - Finds pairs of repeated structures, represented as 
    diagonals of a certain length, k, that start at the same time step as 
    previously found pairs of repeated structures of the same length. 
    
    * find_all_repeats - Finds all the diagonals present in thresh_mat. This 
    function is nearly identical to find_initial_repeats, with two crucial 
    differences. First, we do not remove diagonals after we find them. Second,
    there is no smallest bandwidth size as we are looking for all diagonals.

    * find_complete_list_anno_only - Finds annotations for all pairs of 
    repeats found in find_all_repeats. This list contains all the pairs of  
    repeated structures with their start/end indices and lengths. 
    
    * find_complete_list - Finds all smaller diagonals (and the associated 
    pairs of repeats) that are contained pair_list, which is composed of 
    larger diagonals found in find_initial_repeats.
"""

import numpy as np

def find_add_erows(lst_no_anno, check_inds, k):
    """
    Finds pairs of repeated structures, representated as diagonals of a 
    certain length, k, that end at the same time step as 
    previously found pairs of repeated structures of the same length. 

    Args
    ----
    lst_no_anno: np.array
        list of pairs of repeats
        
    check_inds: np.array
        list of ending indices for repeats of length k that we use 
        to check lst_anno_no for more repeats of length k
        
    k: int
        length of repeats that we are looking for 

    Returns
    -------
    add_rows: np.array
        list of newly found pairs of repeats of length k that are 
        contained in larger repeats in lst_no_anno
    """
    L = lst_no_anno
    # Logical, which pairs of repeats have length greater than k?
    search_inds = (L[:,4] > k)

    # Multiply ending index of all repeats "I" by search_inds
    EI = np.multiply(L[:,1], search_inds)
    # Multipy ending index of all repeats "J" by search_inds
    EJ = np.multiply(L[:,3], search_inds)

    #Loop over check_inds
    for i in range(check_inds.size): 
        #print()
        ci = check_inds[i]
        #print("loop:", i, "ci:", ci)
        
    #Left Check: Check for CI on the left side of the pairs
        # Check if the end index of the repeat "I" equals CI
        lnds = (EI == ci) 
        #print("lnds:", lnds)
        
        # Find new rows 
        if lnds.sum(axis = 0) > 0: #If the sum across (row) is greater than 0 
            # Find the 3rd entry of the row (lnds) whose starting index of 
            # repeat "J" equals CI
            EJ_li = L[lnds,3]
            
            # Number of rows in EJ_li 
            l_num = EJ_li.shape[0] 
            #print("l_num:", l_num)
            
            # Found pair of repeats on the left side
            one_lsi = L[lnds,1] - k + 1     #Starting index of found repeat i
            one_lei = L[lnds,1]             #Ending index of found repeat i
            one_lsj = EJ_li - k + 1         #Starting index of found repeat j
            one_lej = EJ_li                 #Ending index of found repeat j
            one_lk = k*np.ones((l_num,1))   #Length of found pair of repeats
            l_add = np.concatenate((one_lsi, one_lei, one_lsj, one_lej, \
                                    one_lk), axis = None)

            
            # Found pair of repeats on the right side
            two_lsi = L[lnds,0]             #Starting index of found repeat i 
            two_lei = L[lnds,1] - k         #Ending index of ofund repeat i
            two_lsj = L[lnds,2]             #Starting index of found repeat j 
            two_lej = EJ_li - k             #Ending index of found repeat j
            two_lk = L[lnds, 4] - k         #Length of found pair of repeats 
            l_add_left = np.concatenate((two_lsi, two_lei, two_lsj, two_lej,\
                                         two_lk), axis = None)
            
            # Stack the found rows vertically 
            add_rows = np.vstack((l_add, l_add_left))
            
            # Stack all the rows found on the left side of the pairs 
            add_rows = np.concatenate((add_rows, add_rows), axis = 0)
            
    #Right Check: Check for CI on the right side of the pairs
        # Check if the end index of the right repeat of the pair equals CI
        rnds = (EJ == ci)
        
        # Find new rows
        if rnds.sum(axis = 0) > 0:
            # Find the 1st entry of the row whose ending index of repeat 
            # "I" equals CI
            EI_ri = L[rnds, 1]
            # Number of rows in EJ_ri                    
            r_num = EI_ri.shape[0]
                               
            # Found pair of repeats on the left side 
            one_rsi = EI_ri - k + 1         #Starting index of found repeat i 
            one_rei = EI_ri                 #Ending index of found repeat i 
            one_rsj = L[rnds, 3] - k + 1    #Starting index of found repeat j
            one_rej = L[rnds,3]             #Ending index of found repeat j 
            one_rk = k*np.ones((r_num, 1))  #Length of found pair or repeats
            r_add = np.concatenate((one_rsi, one_rei, one_rsj, one_rej, \
                                    one_rk), axis = None)
            
            # Found pairs on the right side 
            two_rsi = L[rnds, 0]            #Starting index of found repeat i  
            two_rei = EI_ri - k             #Ending index of found repeat i 
            two_rsj = L[rnds, 2]            #Starting index of found repeat j
            two_rej = L[rnds, 3] - k        #Ending index of found repeat j 
            two_rk = L[rnds, 4] - k         #Length of found pair or repeats
            r_add_right = np.concatenate((two_rsi, two_rei, two_rsj, two_rej,\
                                          two_rk), axis = None) 
            
            # Stack the found rows vertically 
            add_rows = np.vstack((r_add, r_add_right))
            
            # Stack all the rows found on the right side of the pairs 
            add_rows = np.concatenate((add_rows, add_rows),\
                                      axis = 0).astype(int)
                 
    return add_rows

def find_add_mrows(lst_no_anno, check_inds, k): 
    """
    Finds pairs of repeated structures, represented as diagonals of a certain
    length, k, that neither start nor end at the same time steps as previously
    found pairs of repeated structures of the same length. 

    Args
    ----
        lst_no_anno: np.array 
            list of pairs of repeats

        check_inds: np.array
            list of ending indices for repeats of length k that we use to 
            check lst_no_anno for more repeats of length k 

        k: number
            length of repeats that we are looking for 

    Returns
    -------
        add_rows: np.array
            list of newly found pairs of repeats of length K that are 
            contained in larger repeats in LST_NO_ANNO 
    """
    #Initialize list of pairs 
    L = lst_no_anno 
    
    #Logical, which pair of repeats has a length greater than k 
    search_inds = (L[:,4] > k)
    
    #Multiply the starting index of all repeats "I" by search_inds
    SI = np.multiply(L[:,0], search_inds)

    #Multiply the starting index of all repeats "J" by search_inds
    SJ = np.multiply(L[:,2], search_inds)

    #Multiply the ending index of all repeats "I" by search_inds
    EI = np.multiply(L[:,1], search_inds)

    #Multiply the ending index of all repeats "J" by search_inds
    EJ = np.multiply(L[:,3], search_inds)
    
    #Loop over check_inds 
    for i in range(check_inds.size): 
        ci = check_inds[i]
        #Left Check: check for CI on the left side of the pairs
        lnds = ((SI < ci) + (EI > (ci + k -1)) == 2)
        
        #Check that SI < CI and that EI > (CI + K - 1) indicating that there
        #is a repeat of length k with starting index CI contained in a larger
        #repeat which is the left repeat of a pair
        if lnds.sum(axis = 0) > 0:
            #Find the 2nd entry of the row (lnds) whose starting index of the
            #repeat "I" equals CI 
            SJ_li = L[lnds,2]
            EJ_li = L[lnds,3]
            l_num = SJ_li.shape[0]

            #Left side of left pair
            l_left_k = ci*np.ones(l_num,1) - L[lnds,0]
            l_add_left = np.concatenate((L[lnds,0], (ci - 1 * \
                                         np.ones((l_num,1))), SJ_li, \
    (SJ_li + l_left_k - np.ones((l_num,1))), l_left_k), axis = None)

            #Middle of left pair
            l_add_mid = np.concatenate(((ci*np.ones((l_num,1))), \
                                        (ci+k-1)*np.ones((l_num,1)), \
                                        SJ_li + l_left_k, SJ_li + \
                                        l_left_k + (k-1)*np.ones((l_num,1)),\
                                        k*np.ones((l_num,1))), axis = None) 

            #Right side of left pair
            l_right_k = np.concatenate((L[lnds, 1] - ((ci + k) - 1) * \
                                        np.ones((l_num,1))), axis = None)
            l_add_right = np.concatenate((((ci + k)*np.ones((l_num,1))), \
                                          L[lnds,1], (EJ_li - l_right_k + \
                                           np.ones((l_num,1))), EJ_li, \
                                           l_right_k), axis = None)

            # Add the found rows        
            add_rows = np.vstack((l_add_left, l_add_mid, l_add_right))
            #add_rows = np.reshape(add_rows, (3,5))

        #Right Check: Check for CI on the right side of the pairs
        rnds = ((SJ < ci) + (EJ > (ci + k - 1)) == 2); 

        #Check that SI < CI and that EI > (CI + K - 1) indicating that there
        #is a repeat of length K with starting index CI contained in a larger
        #repeat which is the right repeat of a pair
        if rnds.sum(axis = 0) > 0:
            SI_ri = L[rnds,0]
            EI_ri = L[rnds,1]
            r_num = SI_ri.shape[0]

            #Left side of right pair
            r_left_k = ci*np.ones((r_num,1)) - L[rnds,2]
            r_add_left = np.concatenate((SI_ri, (SI_ri + r_left_k - \
                                                 np.ones((r_num,1))), \
                                              L[rnds,3], (ci - 1) * \
                                              np.ones((r_num,1)), r_left_k), \
                                              axis = None)

            #Middle of right pair
            r_add_mid = np.concatenate(((SI_ri + r_left_k),(SI_ri + r_left_k \
                                        + (k - 1)*np.ones((r_num,1))), \
                                        ci*np.ones((r_num,1)), \
                                        (ci + k - 1)*np.ones((r_num,1)), \
                                        k*np.ones((r_num,1))), axis = None)

            #Right side of right pair
            r_right_k = L[rnds, 3] - ((ci + k) - 1)*np.ones((r_num,1))
            r_add_right = np.concatenate((EI_ri - r_right_k + \
                                          np.ones((r_num,1)),EI_ri,\
                                          (ci + k)*np.ones((r_num,1)), \
                                          L[rnds,3], r_right_k), axis = None)

            add_rows = np.vstack((r_add_left, r_add_mid, r_add_right))
            #add_rows = np.reshape(add_rows, (3,5))

            add_rows = np.concatenate((add_rows, add_rows), \
                                      axis = 0).astype(int)
     
    return add_rows 

def find_add_srows(lst_no_anno, check_inds, k):
    """
    Finds pairs of repeated structures, representated as diagonals of a 
    certain length, k, that start at the same time step as previously found 
    pairs of repeated structures of the same length. 
        
    Args
    ----
    lst_no_anno: np.array 
        list of pairs of repeats
        
    check_inds: np.array
        list of ending indices for repeats of length k that we 
        use to check lst_no_anno for more repeats of length k 
       
    k: int
        length of repeats that we are looking for
            
    Returns
    -------
    add_rows: np.array
        List of newly found pairs of repeats of length K that are 
        contained in larger repeats in lst_no_anno
            
    """

    # Logical, which pair of repeats has a length greater than k 
    search_inds = (L[:,4] > k)

    # Multipy the starting index of all repeats "I" by search_inds
    SI = np.multiply(L[:,0], search_inds)

    # Multiply the starting index of all repeats "J" by search_inds
    SJ = np.multiply(L[:,2], search_inds)

    # Loop over check_inds
    for i in range(check_inds.size):
        ci = check_inds[i] 
            
    # Left check: check for CI on the left side of the pairs 
        # Check if the starting index of repeat "I" of pair of repeats "IJ" 
        # equals CI
        lnds = (SI == ci) 
        print("lnds:", lnds)
        
        # If the sum across (row) is greater than 0 
        if lnds.sum(axis = 0) > 0: 
            # Find the 2nd entry of the row (lnds) whose starting index of 
            # repeat "I" equals CI 
            SJ_li = L[lnds, 2] 
            
            # Used for the length of found pair of repeats 
            l_num = SJ_li.shape[0] 

            # Found pair of repeats on the left side 
            one_lsi = L[lnds, 0]            #Starting index of found repeat i
            one_lei = L[lnds, 0] + k - 1    #Ending index of found repeat i
            one_lsj = SJ_li                 #Starting index of found repeat j
            one_lej = SJ_li + k - 1         #Ending index of found repeat j
            one_lk = np.ones((l_num, 1))*k  #Length of found pair of repeats
            l_add = np.concatenate((one_lsi, one_lei, one_lsj, one_lej,\
                                    one_lk), axis = None)
            
            # Found pair of repeats on the right side 
            two_lsi = L[lnds, 0] + k        #Starting index of found repeat i 
            two_lei = L[lnds, 1]            #Ending index of ofund repeat i
            two_lsj = SJ_li + k             #Starting index of found repeat j 
            two_lej = L[lnds, 3]            #Ending index of found repeat j
            two_lk = L[lnds, 4] - k         #Length of found pair of repeats
            l_add_right = np.concatenate((two_lsi, two_lei, two_lsj, two_lej,\
                                          two_lk), axis = None)
            
            # Stack the found rows vertically 
            add_rows = np.vstack((l_add, l_add_right))
            
            # Stack all the rows found on the left side of the pairs 
            add_rows = np.concatenate((add_rows, add_rows), axis = 0)
            
    # Right Check: check for CI on the right side of the pairs 
        # Check if the the starting index of repeat "J" of the pair "IJ" 
        # equals CI
        rnds = (SJ == ci) 

        if rnds.sum(axis = 0) > 0:
            SJ_ri = L[rnds, 0]
            r_num = SJ_ri.shape[0] 
          
            # Found pair of repeats on the left side 
            one_rsi = SJ_ri                 #Starting index of found repeat i 
            one_rei = SJ_ri + k - 1         #Ending index of found repeat i 
            one_rsj = L[rnds, 2]            #Starting index of found repeat j
            one_rej = L[rnds, 2] + k - 1    #Ending index of found repeat j 
            one_rk = k*np.ones((r_num, 1))  #Length of found pair or repeats
            r_add = np.concatenate((one_rsi, one_rei, one_rsj, one_rej, \
                                    one_rk), axis = None)
            
            # Found pairs on the right side 
            two_rsi = SJ_ri + k             #Starting index of found repeat i  
            two_rei = L[rnds, 1]            #Ending index of found repeat i 
            two_rsj = L[rnds, 2] + k        #Starting index of found repeat j
            two_rej = L[rnds,3]             #Ending index of found repeat j 
            two_rk = L[rnds, 4] - k         #Length of found pair or repeats
            r_add_right = np.concatenate((two_rsi, two_rei, two_rsj, two_rej,\
                                          two_rk), axis = None) 
            
            # Stack the found rows vertically 
            add_rows = np.vstack((r_add, r_add_right))
            
            # Stack all the rows found on the right side of the pairs 
            add_rows = np.concatenate((add_rows, add_rows),\
                                      axis = 0).astype(int)
            
    return add_rows 

def find_all_repeats(thresh_mat,band_width_vec):
    """
    Finds all the diagonals present in thresh_mat. This function is 
        nearly identical to find_initial_repeats, with two crucial 
        differences. First, we do not remove diagonals after we 
        find them. Second, there is no smallest bandwidth size 
        as we are looking for all diagonals.
        
    Args
    ----
    thresh_mat: np.array
        thresholded matrix that we extract diagonals from
    
    band_width_vec: np.array
        vector of lengths of diagonals to be found
    
    Returns
    -------
    all_lst: np.array
        list of pairs of repeats that correspond to diagonals
        in thresh_mat
        
    """
    # Initialize the input and temporary variables
    thresh_temp = thresh_mat
    b = np.size(band_width_vec, axis=0)
    
    int_all = []  # Interval list for non-overlapping pairs
    sint_all = [] # Interval list for the left side of the overlapping pairs
    eint_all = [] # Interval list for the right side of the overlapping pairs
    mint_all = [] # Interval list for the middle of the overlapping pairs if 
                  # they exist
    
    for i in range(1, b + 1): # Loop over all possible band_widths
        # Set current band_width
        j = b - i + 1
        band_width = band_width_vec[j - 1]

        # Search for diagonals of length band_width
        DDM = signal.convolve2d(thresh_temp[0:,0:],np.eye(band_width),\
                                'valid').astype(int)

        # Mark where diagonals of length band_width start
        thresh_DDM = (DDM == band_width)

        if thresh_DDM.sum() > 0:
            full_band_width = band_width
            # 1) Non-Overlaps: Search outside the overlapping shingles
            # Find the starts that are paired together
            find_starts = np.nonzero(np.triu(thresh_DDM,full_band_width))
            start_I = np.array(find_starts[0])
            start_J = np.array(find_starts[1])
            num_nonoverlaps = start_I.shape[0]

            # Find the matching ends EI for SI and EJ for SJ
            end_I = start_I + (full_band_width - 1)
            end_J = start_J + (full_band_width - 1)

            # List pairs of starts with their ends and the widths of the
            # non-overlapping intervals
            int_lst = np.column_stack([start_I, end_I, start_J, end_J, \
                                       full_band_width * \
                                       np.ones((num_nonoverlaps, 1))]).astype(int)

            # Add the new non-overlapping intervals to the full list of
            # non-overlapping intervals
            int_all.append(int_lst)

            # 2) Overlaps: Search only the overlaps in shingles
            overlap_shingles = np.nonzero(np.tril(np.triu(thresh_DDM,1),\
                                                  (full_band_width - 1)))
            start_I_overlap = np.array(overlap_shingles[0])
            start_J_overlap = np.array(overlap_shingles[1])
            num_overlaps = start_I_overlap.shape[0]

            if num_overlaps > 0:
                # Since you are checking the overlaps you need to cut these
                # intervals into pieces: left, right, and middle. NOTE: the
                # middle interval may NOT exist

                # Vector of 1's that is the length of the number of
                # overlapping intervals. This is used a lot.
                ones_no = np.ones((num_overlaps,1)).astype(int)

                # 2a) Left Overlap
                K = start_J_overlap - start_I_overlap  
                # NOTE: end_J_overlap - end_I_overlap will also equal this,
                               # since the intervals that are overlapping are
                               # the same length. Therefore the "left"
                               # non-overlapping section is the same length as
                               # the "right" non-overlapping section. It does
                               # NOT follow that the "middle" section is equal
                               # to either the "left" or "right" piece. It is
                               # possible, but unlikely.
                sint_lst = np.column_stack([start_I_overlap,(start_J_overlap \
                            - ones_no),start_J_overlap,(start_J_overlap + K - ones_no),K]).astype(int)
                Is = np.argsort(K) # Return the indices that would sort K
                Is.reshape(np.size(Is), 1)
                sint_lst = sint_lst[Is,]

                # Add the new left overlapping intervals to the full list
                # of left overlapping intervals
                sint_all.append(sint_lst)

                # 2b) Right Overlap
                end_I_overlap = start_I_overlap + (full_band_width-1)
                end_J_overlap = start_J_overlap + (full_band_width-1)
                eint_lst = np.column_stack([(end_I_overlap + ones_no - K), end_I_overlap,(end_I_overlap + ones_no), end_J_overlap, K]).astype(int)
                Ie = np.argsort(K) # Return the indices that would sort K
                Ie.reshape(np.size(Ie),1)
                eint_lst = eint_lst[Ie,:]

                # Add the new right overlapping intervals to the full list of
                # right overlapping intervals
                eint_all.append(eint_lst)
                
                # 2) Middle Overlap
                mnds = (end_I_overlap - start_J_overlap - K + ones_no) > 0
                start_I_middle = start_J_overlap * (mnds)
                end_I_middle = (end_I_overlap*(mnds) - K*(mnds))
                start_J_middle = (start_J_overlap*(mnds) + K*(mnds))
                end_J_middle = end_I_overlap*(mnds)
                k_middle = (end_I_overlap*(mnds) - start_J_overlap*(mnds) - K*(mnds) + ones_no*(mnds))
            
                if mnds.sum() > 0:
                    mint_lst = np.column_stack([start_I_middle,end_I_middle,start_J_middle,end_J_middle,k_middle])
                    Im = np.argsort(k_middle)
                    Im.reshape(np.size(Im),1)
                    mint_lst = mint_lst[Im,:]

                    # Add the new middle overlapping intervals to the full list
                    # of middle overlapping intervals
                    mint_all.append(mint_lst)

        if thresh_temp.sum() == 0:
            break 
        
    out_lst = sint_all + eint_all + mint_all + int_all
    all_lst = filter(None,out_lst)

    if out_lst is not None:
        all_lst = np.vstack(out_lst)
    else:
        all_lst = np.array([])

    return all_lst

def find_complete_list_anno_only(pair_list, song_length):
    """
    Finds annotations for all pairs of repeats found in find_all_repeats. This 
    list contains all the pairs of repeated structures with their start/end 
    indices and lengths.
    
    Args
    ----
    pair_list: 
        list of pairs of repeats
        WARNING: bandwidths must be in ascending order
        
    song_length: int
        number of audio shingles in song
        
    Returns
    -------
    out_lst:
        list of pairs of repeats with smaller repeats added and with
        annotation markers
    """
    # Find list of unique repeat lengths
    bw_found = np.unique(pair_list[:,4])
    bw_num = bw_found.shape[0]
    
    # Remove longest bandwidth row if it is the length of the full song
    if song_length == bw_found[bw_num - 1]:
        pair_list[-1,:] = []
        bw_found[-1] = []
        bw_num = (bw_num - 1)
    p = pair_list.shape[0]
    
    # Add annotation markers to each pair of repeats
    full_list = []
    for j in range(bw_num):
        band_width = bw_found[j]
        # Isolate pairs of repeats of desired length
        bsnds = np.amin(np.nonzero(pair_list[:,4] == band_width))
        bends = np.nonzero(pair_list[:,4] > band_width)
        
        if np.size(bends) > 0:
            bends = np.amin(bends)
        else:
            bends = p
        
        bw_mat = np.array((pair_list[bsnds:bends,]))
        bw_mat_length = bw_mat.shape[0]
        
        temp_anno_mat = np.concatenate((bw_mat,(np.zeros((bw_mat_length,1)))),\
                                       axis = 1).astype(int)

        # Get annotations for this bandwidth
        temp_anno_list = add_annotations(temp_anno_mat, song_length)
        full_list.append(temp_anno_list)
        
    out_list = np.concatenate(full_list)
        
    return out_list

def find_complete_list(pair_list,song_length):
    """
    Finds all smaller diagonals (and the associated pairs of repeats) that are
    contained pair_list, which is composed of larger diagonals found in 
    find_initial_repeats.
        
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
        # Return the minimum of the array
        bsnds = np.amin((pair_list[:,4] == band_width).nonzero())
        bends = (pair_list[:,4] > band_width).nonzero()
    
        # Convert bends into an array
        bend = np.array(bends)
    
        if bend.size > 0:
            bend = np.amin(bend)
        else:
            bend = p
    
        # Part A1: Isolate all starting time steps of the repeats of length 
        # bandwidth
        start_I = pair_list[bsnds:bend, 0]
        start_J = pair_list[bsnds:bend, 2]
        combine_starts = [start_I,start_J]
        
        all_vec_snds = np.concatenate(combine_starts)
        int_snds = np.unique(all_vec_snds)
    
        # Part A2: Isolate all ending time steps of the repeats of length 
        # bandwidth
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
        add_srows = find_add_srows_both_check_no_anno(pair_list, int_snds, \
                                                      band_width)
        add_erows = find_add_mrows_both_check_no_anno(pair_list, int_snds, \
                                                      band_width)
        add_mrows = find_add_erows_both_check_no_anno(pair_list, int_ends, \
                                                      band_width)
        
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
    # Return the indices that would sort combine_mat's fourth column
    combine_inds = np.argsort(combine_mat[:,4]) 
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
        # Return the minimum of the array
        new_bsnds = np.amin((combine_mat[:,4] == new_bw).nonzero()) 
        new_bends = (combine_mat[:,4] > new_bw).nonzero() 

        # Convert new_bends into an array
        new_bend = np.array(new_bends)
    
        if new_bend.size > 0:
            new_bend = np.amin(new_bend)
        else:
            new_bend = c
        
        band_width_mat = np.array((combine_mat[new_bsnds:new_bend,]))
        length_band_width_mat = np.size(band_width_mat,axis=0)

        temp_anno_lst = np.concatenate((band_width_mat,\
                                        (np.zeros((length_band_width_mat,1))))\
            ,axis=1).astype(int)

        # Part C: Get annotation markers for this bandwidth
        temp_anno_lst = add_annotations(temp_anno_lst, song_length)
        full_lst.append(temp_anno_lst)
        final_lst = np.vstack(full_lst)
    
    lst_out = final_lst
    
    return lst_out

import scipy.io as sio
import numpy as np
def csv_to_aligned_hierarchies(file_in, file_out, num_fv_per_shingle, thresh):
    """
    Example of full aligned hierarchies pathway
    
    Args
    ----
    file_in: str
        name of .csv file to be processed. Contains features across time steps to be analyzed
        - example-  chroma features
    
    file_out: str
        name of file where output will be stored
    
    num_fv_per_shingle: int
        number of feature vectors per time step. For chroma this would be 12 as there are 12 notes in the Western scale
        should equal number of rows in input csv file
        
    thresh: int
        maximum threshold value. Largest length repeat to search for.
    
    Returns
    -------
    none: .mat file is saved. Contains variables created for aligned hierarchies. 
    """
    # Import file of feature vectors
    with open(file_in, 'r', newline='\n') as f:
        fv_mat = np.loadtxt(f, delimiter = ',')
    
    # Get pairwise distance matrix/self dissimilarity matrix using cosine distance
    self_dissim_mat = create_sdm(fv_mat, num_fv_per_shingle)
    # Get thresholded distance matrix
    song_length = self_dissim_mat.shape[0]
    thresh_dist_mat = (self_dissim_mat <= thresh) 
    #think this is redund in python * np.ones((song_length,song_length))
    # Extract diagonals from thresholded distance matrix, saving the repeat pairs
    # the diagonals represent

    all_lst = find_initial_repeats(thresh_dist_mat, np.arange(song_length+1), 0)
    print(all_lst)
#     # Find smaller repeats contained within larger repeats
    complete_lst = find_complete_list(all_lst, song_length)

#     # Create dictionary of output variables
    outdict = {}
    outdict['thresh'] = thresh
    
#     if np.size(complete_lst) != 0:
#         # Remove groups of repeats that overlap in time
#         output_tuple = remove_overlaps(complete_lst, song_length)
#         (mat_no_overlaps, key_no_overlaps) = output_tuple[1:3]
        
#         # Distill non-overlapping repeats into essential structure components and
#         # use them to build the hierarchical representation
#         output_tuple = hierarchical_structure(mat_no_overlaps, key_no_overlaps, song_length)
#         (full_key, full_mat_no_overlaps) = output_tuple[1:3]
        
#         outdict['full_key'] = full_key
#         outdict['full_mat_no_overlaps'] = full_mat_no_overlaps
        
#         # Save list of partial representations contatining only the full hierarchical
#         # representation for use in comparison code
#         outdict['partial_reps'] = [full_mat_no_overlaps]
#         outdict['partial_key'] = [full_key]
#         outdict['partial_widths'] = song_length
#         outdict['partial_num_blocks'] = np.sum(mat_no_overlaps)
#         outdict['num_partials'] = 1
        
#         # Create output file
#         sio.savemat(file_out, outdict)
        
#     else:
#         outdict['full_key'] = []
#         outdict['full_mat_no_overlaps'] = []
        
#         # Save empty list of partial representations for use in comparison code
#         outdict['partial_reps'] = []
#         outdict['partial_key'] = []
#         outdict['partial_widths'] = []
#         outdict['partial_num_blocks'] = []
#         outdict['num_partials'] = 0
        
#         # Create output file
#         sio.savemat(file_out, outdict)

        
#run on example file
file_in = "input.csv"
file_out = "hierarchical_out_file.mat"
num_fv_per_shingle = 12
thresh = 10
csv_to_aligned_hierarchies(file_in, file_out, num_fv_per_shingle, thresh)

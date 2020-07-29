import sys, subprocess, os

#---------------Sets up tmin call for each mode---------------#
def full(seed_files, total_files):   
    # Initialises counter
    i = 0     
            
    # Iterates through all files in directory and reduces them to the smallest number of useful bits
    for seed in seed_files:
        # Increments counter
        i += 1
        # Prints test number current-test/total-tests
        print('minimising ' + str(i) + '/' + str(total_files) + '\n')

        # Calls afl-tmin
        subprocess.run(['afl-tmin', '-i', seed, '-o', seed, 'bigrapher', 'full', '-p', '/dev/null', '@@'])
            
    print('Tmin process completed! Have a nice day!')




def sim(seed_files, total_files): 
    # Initialises counter
    i = 0        
         
    # Iterates through all files in directory and reduces them to the smallest number of useful bits
    for seed in seed_files:
        # Increments counter
        i += 1
        # Prints test number current-test/total-tests
        print('minimising ' + str(i) + '/' + str(total_files) + '\n')
        
    print('Tmin process completed! Have a nice day!')




def validate(seed_files, total_files):    
    # Initialises counter
    i = 0     
            
    # Iterates through all files in directory and reduces them to the smallest number of useful bits
    for seed in seed_files:
        # Increments counter
        i += 1
        # Prints test number current-test/total-tests
        print('minimising ' + str(i) + '/' + str(total_files) + '\n')
        
    print('Tmin process completed! Have a nice day!')




#---------------Parsing input---------------#
# Stores the location of the corpus_directory
corpus_directory = sys.argv[1]
# Stores the bigrapher mode to be tested
mode = sys.argv[2]

# Stores an iterator of DirEntry objects
seed_files = os.scandir(corpus_directory)
# Stores the number of seed files
total_files = len(os.listdir(corpus_directory))


#---------------Calling Correct Mode---------------#
if mode == 'full':

    full(seed_files, total_files)
elif mode == 'sim':

    sim(seed_files, total_files)
elif mode == 'validate':

    validate(seed_files, total_files)
else:

    print('Invalid Bigrapher mode please select full, sim or validate.')
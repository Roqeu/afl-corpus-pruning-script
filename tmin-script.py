from subprocess import run
from shutil import move
from sys import argv
from os import listdir, scandir, path, rmdir


#---------------Handles moving files back to parent directory---------------#
# Note: afl expects 1 corpus directory of seed files, this function returns all minimised files to main corpus directory
def copy_back(corpus_directory, parent_directory):
     # Stores seed files as list instead of iterable as allows for easier path creation
    seed_files = listdir(corpus_directory)

    # Loops through corpus directory and copies 
    for seed in seed_files:
        # Creates path of file to be moved
        old_dir = path.join(corpus_directory, seed)
        # Moves file to main corpus directory
        move(old_dir, parent_directory)


    rmdir(corpus_directory)
#---------------Sets up tmin call for each mode---------------#
def full(corpus_directory, parent_directory, total_files):  

    # Stores an iterator of DirEntry objects
    seed_files = scandir(corpus_directory)
    # Initialises counter
    i = 0     
       
    # Iterates through all files in directory and reduces them to the smallest number of useful bits
    for seed in seed_files:
        # Increments counter
        i += 1
        # Prints test number current-test/total-tests
        print('minimising ' + str(i) + '/' + str(total_files) + '\n')

        # Calls afl-tmin
        run(['afl-tmin', '-i', seed, '-o', seed, target, 'full', '-p', '/dev/null', '@@'])
            
    copy_back(corpus_directory, parent_directory)

    print('Tmin process completed! Have a nice day! :)')




def sim(corpus_directory, parent_directory, total_files): 

    # Stores an iterator of DirEntry objects
    seed_files = scandir(corpus_directory)
    # Initialises counter
    i = 0     
       
    # Iterates through all files in directory and reduces them to the smallest number of useful bits
    for seed in seed_files:
        # Increments counter
        i += 1
        # Prints test number current-test/total-tests
        print('minimising ' + str(i) + '/' + str(total_files) + '\n')

        # Calls afl-tmin
        run(['afl-tmin', '-i', seed, '-o', seed, target, 'sim', '-T', '500', '-s', '-t', '/dev/null', '-f', 'svg', '@@'])
            
    copy_back(corpus_directory, parent_directory)

    print('Tmin process completed! Have a nice day! :)')


def validate(corpus_directory, parent_directory, total_files):  
 
    # Stores an iterator of DirEntrseed_filesy objects
    seed_files = scandir(corpus_directory)
    # Initialises counter
    i = 0     
       
    # Iterates through all files in directory and reduces them to the smallest number of useful bits
    for seed in seed_files:
        # Increments counter
        i += 1
        # Prints test number current-test/total-tests
        print('minimising ' + str(i) + '/' + str(total_files) + '\n')

        # Calls afl-tmin
        run(['afl-tmin', '-i', seed, '-o', seed, target, 'validate', '-d', '/dev/null', '-f', 'svg', '@@'])
            
    copy_back(corpus_directory, parent_directory)

    print('Tmin process completed! Have a nice day! :)')




#---------------Parsing input---------------#
# Stores the location of the parent directory to copy minimised files to
parent_directory = argv[1]
# Stores the location of the corpus_directory
corpus_directory = argv[2]
# Stores location of target .exe
target = argv[3]
# Stores the bigrapher mode to be tested
mode = argv[4]
 
# Stores the number of seed files
total_files = len(listdir(corpus_directory))


#---------------Calling Correct Mode---------------#
if mode == 'full':

    full(corpus_directory, parent_directory, total_files)
elif mode == 'sim':

    sim(corpus_directory, parent_directory, total_files)
elif mode == 'validate':

    validate(corpus_directory, parent_directory, total_files)
else:

    print('Invalid Bigrapher mode please select full, sim or validate.')
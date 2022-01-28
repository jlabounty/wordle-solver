import numpy
import pandas 
import os 
import sys
import json
import numpy as np

def load_wordlist(infile):
    this = []
    with open(infile, 'r') as f:
        for line in f:
            if(len(line) > 1):
                this.append(line.strip())

    return this 

def count_letters(input, normalize=True):
    occurances = {}
    for item in input:
        if(item in occurances):
            occurances[item] += 1
        else:
            occurances[item] = 1

    if(normalize):
        sum = np.sum(list(occurances.values()))
        # print(sum)
        if(sum > 0):
            for x in occurances:
                occurances[x] = occurances[x] / sum

    return occurances

def main():
    infile = sys.argv[1]
    assert os.path.exists(infile)

    words = load_wordlist(infile)

    letters = list(zip(*words))
    # print(letters)
    occurances = {i:count_letters(x) for i,x in enumerate(letters)}
    print(occurances)

    outfile = "../data/letter_frequencies_by_place.json"
    with open(outfile, 'w') as fout:
        json.dump(occurances, fout, indent=1, sort_keys=True)
    print("All done, written to:", outfile)




if __name__ == "__main__":
    main()
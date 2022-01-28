from typing import Dict
import pandas 
import numpy as np 
import json

class WordleSolver():
    def __init__(self, data='data/wordle_list.txt', 
                       frequencies='data/letter_frequencies_by_place.json', 
                       verbose=True, weight_by_place=True) -> None:
        self.data = pandas.read_csv(data, header=None,names=['word'] )
        with open(frequencies, 'r') as f:
            self.frequencies = json.load(f)
    
        if(weight_by_place):
            # weighting generated from word list itself based on frequency and position
            self.data['weights'] = self.data['word'].apply(self.get_frequency_of_word_by_position)
        else:
            # simple weighing based on english language
            self.data['weights'] = self.data['word'].apply(self.get_frequency_of_word)
        self.data.sort_values(by='weights', ascending=False, inplace=True)
        self.verbose=verbose

        if(self.verbose):
            print("Weighting with frequencies:")
            print(self.frequencies)
        if(self.verbose):
            print("Word list:")
            print(self.data.head())

        self.data_orig = self.data.copy()

    def reset(self):
        self.data = self.data_orig.copy()


    def get_frequency_of_word(self,word):
        # word = word.split("")[1:-1]
        # print(word)
        word = list(set(word)) #don't weight the same letter more than once
        weights = [self.frequencies[x] for x in word]
        # print(weights)
        return np.sum(weights)

    def get_frequency_of_word_by_position(self,word):
        # word = word.split("")[1:-1]
        # print(word)
        word = list(set(word)) #don't weight the same letter more than once
        weights = [self.frequencies[str(i)][x] if x in self.frequencies[str(i)] else 0 for i,x in enumerate(word)]
        # print(weights)
        return np.sum(weights)

    def guess(self):
        try:
            guess = self.data['word'].iloc[0]
            if(self.verbose):
                print("New guess:", guess)
            return guess
        except:
            raise ValueError("ERROR: No word found matching these conditions!")

    def eval_guess(self, truth, guess):
        exact = ''
        doesnt_contain = ''
        contains = {}
        
        for i, x in enumerate(guess):
            if(x == truth[i]):
                exact += x 
            elif x in truth:
                exact += '.'
                contains[x] = [i]
            else:
                doesnt_contain += x
                exact += '.'

        return exact, contains, doesnt_contain



    def parse_guess(self, exact='.....', contains=Dict, doesnt_contain=''):
        '''
            Parse the output of a wordle guess
            exact
                This letter is exactly here: ...w. -> there is a w in position 4
            contains
                This word contains this letter: {'a':[4], 'q':[1]} -> there is an a and a q 
                    somewhere in the word, NOT in position 4/1 though
        '''
        if(self.verbose):
            print(f"Starting with {self.data.shape[0]} words in list")

        # first parse the exact matches
        for i, letter in enumerate(exact):
            if(letter != '.'):
                self.data = self.data.loc[self.data['word'].str[i] == letter]

        for letter, guessed_positions in contains.items():
            self.data = self.data.loc[self.data['word'].str.contains(letter)]
            for posi in guessed_positions:
                self.data = self.data.loc[ self.data['word'].str[posi] != letter ]

        for letter in doesnt_contain:
            self.data = self.data.loc[~self.data['word'].str.contains(letter)]

        if(self.verbose):
            print(f"{self.data.shape[0]} words remaining")

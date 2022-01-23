from email import header
from typing import Dict
import pandas 
import numpy as np 
import json

class WordleSolver():
    def __init__(self, data='data/wordle_list.txt', frequencies='data/letter_frequencies.json') -> None:
        self.data = pandas.read_csv(data, header=None,names=['word'] )
        with open(frequencies, 'r') as f:
            self.frequencies = json.load(f)
        # self.data['weights'] = 
        print(self.frequencies)
        self.data['weights'] = self.data['word'].apply(self.get_frequency_of_word)
        self.data.sort_values(by='weights', ascending=False, inplace=True)

        print(self.data.head())


    def get_frequency_of_word(self,word):
        # word = word.split("")[1:-1]
        # print(word)
        word = list(set(word)) #don't weight the same letter more than once
        weights = [self.frequencies[x] for x in word]
        # print(weights)
        return np.sum(weights)

    def guess(self):
        try:
            return self.data['word'].iloc[0]
        except:
            raise ValueError("ERROR: No word found matching these conditions!")

    def parse_guess(self, exact='.....', contains=Dict, doesnt_contain=''):
        '''
            Parse the output of a wordle guess
            exact
                This letter is exactly here: ...w. -> there is a w in position 4
            contains
                This word contains this letter: {'a':[4], 'q':[1]} -> there is an a and a q 
                    somewhere in the word, NOT in position 4/1 though
        '''
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

        print(f"{self.data.shape[0]} words remaining")

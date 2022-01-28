from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from solver import *
from selenium.webdriver.common.by import By
import time

class WordlePlayer():

    def __init__(self, verbose=False) -> None:
        self.verbose=verbose

    def setUp(self):
        # set up the web driver to open the wordle site
        self.driver = webdriver.Firefox()

    def play(self):
        # open the site and click out of the how-to
        driver = self.driver
        driver.get("https://www.powerlanguage.co.uk/wordle/")
        time.sleep(1)
        Elem = driver.find_element_by_tag_name('html')
        Elem.click()
        time.sleep(1)


        # get the relevent objects to be able to parse our guesses
        game_app = driver.find_element_by_tag_name('game-app')
        board = driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app)
        game_rows = board.find_elements_by_tag_name('game-row')
        rows = [driver.execute_script("return arguments[0].shadowRoot.children[1]", x) for x in game_rows]
        # print('rows:', rows)

        solver = WordleSolver(verbose=self.verbose)
        for guess in range(6):
            this_guess = solver.guess()
            if(self.verbose):
                print(f"Starting guess {guess} -> {this_guess}")
            Elem.send_keys(this_guess)
            Elem.send_keys(Keys.ENTER)

            time.sleep(2)
            result = self.parse_row(rows[guess])
            if(self.verbose):
                print('   -> parsed with result:', result)
            if('.' not in result[0]):
                print(f"We did it in {guess+1} guesses! The word is:", result[0])
                break

            #update the word list with this information and prepate the next guess
            solver.parse_guess(*result)

            # input("so?")

    def parse_row(self, row):
        '''using the html from the tile objects, see how our guess did'''
        html = row.get_attribute('innerHTML')

        exact = ''
        absent = ''
        wrong_positon = {}

        for i,tile in enumerate(html.split("</game-tile>")[:-1]):
            # print(tile)
            letter = tile.split('letter="')[1].split('"')[0]
            evaluation = tile.split('evaluation="')[1].split('"')[0]
            # print(letter, evaluation)
            if(evaluation=='absent'):
                absent += letter
                exact += '.'
            elif(evaluation=='present'):
                wrong_positon[letter] = [i]
                exact += '.'
            elif(evaluation=='correct'):
                exact += letter

            for x in exact:
                if(x in absent):
                    absent = absent.replace(x,'')

        return exact, wrong_positon, absent

    def tearDown(self):
        self.driver.close()

def main():
    player = WordlePlayer(verbose=True)
    player.setUp()
    player.play()
    input("What do you think?")
    player.tearDown()
    print("See you tomorrow!")



if __name__ == "__main__":
    main()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from solver import *
from selenium.webdriver.common.by import By
import time

class WordlePlayer():

    def setUp(self):
        self.driver = webdriver.Firefox()

    def play(self):
        driver = self.driver
        driver.get("https://www.powerlanguage.co.uk/wordle/")
        # self.assertIn("Python", driver.title)
        # time.sleep(5)

        time.sleep(1)

        Elem = driver.find_element_by_tag_name('html')

        Elem.click()

        time.sleep(1)

        # driver.click("game-app::shadow game-modal::shadow game-icon")


        game_app = driver.find_element_by_tag_name('game-app')
        board = driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app)
        game_rows = board.find_elements_by_tag_name('game-row')
        rows = [driver.execute_script("return arguments[0].shadowRoot.children[1]", x) for x in game_rows]
        # print('rows:', rows)

        solver = WordleSolver()
        for guess in range(6):
            this_guess = solver.guess()
            # print(f"Starting guess {guess} -> {this_guess}")
            Elem.send_keys(this_guess)
            Elem.send_keys(Keys.ENTER)

            time.sleep(2)
            result = self.parse_row(rows[guess])
            # print(result)
            if('.' not in result[0]):
                print(f"We did it in {guess+1} guesses! The word is:", result[0])
                break
            solver.parse_guess(*result)

            # input("so?")

    def parse_row(self, row):
        # print("Parsing row:", row)
        # print("   ->", row.tag_name, row.get_attribute("value"), row.text)
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

        return exact, wrong_positon, absent
            


    def tearDown(self):
        self.driver.close()

# def main():
player = WordlePlayer()
player.setUp()
player.play()

    # return player


# if __name__ == "__main__":
#     main()
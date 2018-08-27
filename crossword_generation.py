from dictionary import word_dictionary
from crossword import Crossword
import random 

test_word1 = word_dictionary[random.randint(0,52250)]
test_word2 = word_dictionary[random.randint(0,52250)]
test_word3 = word_dictionary[random.randint(0,52250)]



def check_direction(spots):
    if spots[0][0] != spots[0][1]:
        return 'down'
    else:
        return 'across'

cw = Crossword()
possible_spots1 = cw.board.get_sequences(len(test_word1))
possible_spots2 = cw.board.get_sequences(len(test_word2))
possible_spots3 = cw.board.get_sequences(len(test_word3))

if possible_spots1:
    cw.insert_word(test_word1, possible_spots1[0], check_direction(possible_spots1[0]))
if possible_spots2:
    cw.insert_word(test_word2, possible_spots2[0], check_direction(possible_spots2[0]))
if possible_spots3:
    cw.insert_word(test_word3, possible_spots3[0], check_direction(possible_spots3[0]))
cw.visualize()
print(cw.words.across, cw.words.down)


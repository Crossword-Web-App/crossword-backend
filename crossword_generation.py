from dictionary import word_dictionary
from crossword import Crossword
import random

words = []
for _ in range(52250):
    words.append(word_dictionary[random.randint(0,52250)])

cw = Crossword()

for word in words:
    valid_sequences = cw.find_available_sequences_for_word(word)
    print(valid_sequences)
    if len(valid_sequences) > 0:
        selected_sequence = valid_sequences[random.randint(0, len(valid_sequences) - 1)]
        cw.insert_word(word, selected_sequence, cw.get_word_direction(selected_sequence))
    else:
        print('no valid sequence')

cw.visualize()
print(cw.words.across, cw.words.down)


# highest-level crossword class, encompasses all

class Crossword:

    def __init__(self):
        # doesn't know the board, just the words
        self.words = Word_Storage()
        # doesn't know the words, just the letters and blank spots
        self.board = Board_Storage()

    def get_word_direction(self, word):
        if word[0][0] == word[1][0]:
            return 'across'
        return 'down'

    def get_letter_at_coords(self, coords):
        return self.board.cw_dict[coords[0]][coords[1]]

    def find_available_sequences_for_word(self, word):
        valid_sequences = []
        candidate_sequences = self.board.get_sequences(len(word))

        # TODO: create ranking system for best placement
        for sequence in candidate_sequences:
            valid_word = True
            idx = 0
            while idx < len(sequence) and valid_word:
                if self.get_letter_at_coords(sequence[idx]) != '' and self.get_letter_at_coords(sequence[idx]) != word[idx]:
                    valid_word = False
                idx += 1
            if valid_word:
                valid_sequences.append(sequence)

        return valid_sequences


    # put word in both word_storage and crossword_dict
    def insert_word(self, word, coords, direction):

        # adding to word storage
        self.words.add_word(word, coords, direction)

        # adding to board storage
        for idx, coord in enumerate(coords):
            x, y = coord
            self.board.cw_dict[x][y] = word[idx]

    def delete_word(self, word, coords, direction):

        # removing from word storage
        self.words.del_word(word, coords, direction)

        # removing from board storage
        for coord in coords:
            x, y = coord
            self.board.cw_dict[x][y] = ''

        pass

    # helper function to show crossword as it currently exists, for testing
    def visualize(self):
        for column in self.board.cw_dict:
            new_row = ''
            for row in self.board.cw_dict[column]:
                if self.board.cw_dict[column][row] == '':
                    new_row += " _ "
                else:
                    new_row += " " + self.board.cw_dict[column][row] + " "
            print(new_row, '\n')
        pass


class Board_Storage:

    def __init__(self):
        self.cw_dict = self.setup_crossword()
        self.generate_board_with_black_squares()
        self.sequences_dict = self.setup_sequences_dict()

    def setup_crossword(self):
        columndict = {}
        for num in range(0,15):
            rowdict = {}
            for rownum in range(0,15):
                rowdict[rownum] = ''
            columndict[num] = rowdict
        return columndict

    def setup_sequences_dict(self):
        # across
        seq_dict = {}

        for row_idx, row in enumerate(self.cw_dict):
            temp = []
            end_of_word = False
            for col_idx, column in enumerate(self.cw_dict[row]):
                if self.cw_dict[row][column] == '#':
                    end_of_word = True
                elif col_idx == len(self.cw_dict[row])-1:
                    temp.append((row_idx, col_idx))
                    end_of_word = True
                if end_of_word:
                    if len(temp) > 0:
                        if len(temp) in seq_dict.keys():
                            seq_dict[len(temp)].append(temp)
                        else:
                            seq_dict[len(temp)] = [temp]
                    temp = []
                    end_of_word = False
                else:
                    temp.append((row_idx, col_idx))


        for col_idx in range(0,len(self.cw_dict)-1):
            temp = []
            end_of_word = False
            for row_idx in range(0, len(self.cw_dict)-1):
                if self.cw_dict[row_idx][col_idx] == '#':
                    end_of_word = True
                elif row_idx == len(self.cw_dict[row])-1:
                    temp.append((row_idx, col_idx))
                    end_of_word = True
                if end_of_word:
                    if len(temp) > 0:
                        if len(temp) in seq_dict.keys():
                            seq_dict[len(temp)].append(temp)
                        else:
                            seq_dict[len(temp)] = [temp]
                    temp = []
                    end_of_word = False
                else:
                    temp.append((row_idx, col_idx))

        return seq_dict

    # 'get all sequences where num of chars = x' in board
    # get_sequences(3) will return a list of every 3 sequence in the board
    def get_sequences(self, num):
        if num in self.sequences_dict.keys():
            return self.sequences_dict[num]
        else:
            return {}

# store word by coordinates, wordid
# add 'number' as last step, once we've figured out the puzzle works
# add_word('hey', [(0,0), (0,1), (0,2)], down)

    def generate_board_with_black_squares(self):
        import random
        black_range = [34, 36, 38, 40, 42]
        num_black_squares = black_range[random.randint(0,4)]

        def get_diag(tup):
            x,y = tup
            return (abs(14-x),abs(14-y))

        left_triangle = []
        column = 15
        for x in range(0,15):
            for y in range(0,column):
                tup = (x,y)
                left_triangle.append(tup)
            column -= 1

        def check_if_free(coords, cw_dict):
            x, y = coords

                #returns false for black sqs and things outside the boundary
            def dict_get(x,y):
                try:
                    if self.cw_dict[x][y] == '':
                        return True
                    else:
                        return False
                except:
                    return False

            one_up = dict_get(x-1, y)
            two_up = dict_get(x-2, y)
            three_up = dict_get(x-3, y)
            one_left = dict_get(x, y-1)
            two_left = dict_get(x, y-2)
            three_left = dict_get(x, y-3)
            one_right = dict_get(x, y+1)
            two_right = dict_get(x, y+2)
            three_right = dict_get(x, y+3)
            one_down = dict_get(x+1, y)
            two_down = dict_get(x+2, y)
            three_down = dict_get(x+3, y)

            # if something 3 up is either black or the boundary, but two and one up are both free
            if three_up == False and two_up == True and one_up == True:
                return False
            # if something 2 up is either one or the boundary, and one up is free
            if two_up == False and one_up == True:
                return False

            if three_down == False and two_down == True and one_down == True:
                return False
            if two_down == False and one_down == True:
                return False

            if three_right == False and two_right == True and one_right == True:
                return False
            if two_right == False and one_right == True:
                return False

            if three_left == False and two_left == True and one_left == True:
                return False
            if two_left == False and one_left == True:
                return False
            return True

        num = 0
        idx = 0

        while num < num_black_squares:
            tup = left_triangle[idx]
            die = random.randint(0,5)
            if die == 5:
                if check_if_free(tup, self.cw_dict):
                    x, y = tup
                    if self.cw_dict[x][y] is not '#':
                        self.cw_dict[x][y] = '#'
                        if check_if_free(get_diag(tup), self.cw_dict):
                            x2, y2 = get_diag(tup)
                            self.cw_dict[x2][y2] = '#'
                            num += 2
                        else:
                            self.cw_dict[x][y] = ''
            if idx >= len(left_triangle) - 1:
                idx = 0
            else:
                idx += 1

class Word_Storage:

    def __init__(self):
        self.across = {}
        self.down = {}

    def add_word(self, word, cords, direction):
        if direction == 'across':
            self.across[word] = cords
        else:
            self.down[word] = cords

    def del_word(self, word, cords, direction):
        if direction == 'across':
            del self.across[word]
        else:
            del self.down[word]

# testcw = Crossword()
# testcw.insert_word('HEY', [(0,0), (1,0), (2,0)], 'down')
# print(testcw.words.down)
# testcw.delete_word('HEY', [(0,0), (1,0), (2,0)], 'down')
# print(testcw.words.down)

# testcw.visualize()



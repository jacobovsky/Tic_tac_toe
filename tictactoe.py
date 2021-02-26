import sys
import random
import math


def get_new_table_after_move(table_state, move_index, player_symbol):
    table_state_list = list(table_state)
    table_state_list[move_index] = player_symbol
    return ''.join(table_state_list)


def add_spaces_to_initial_input(initial_input):
    initial_input = list(initial_input)
    modified_input = ''
    for char in initial_input:
        modified_input += char + ' '
    return modified_input[:-1]


def get_symbol_for_player(initial_shape):
    amount_of_o = 0
    amount_of_x = 0
    for char in initial_shape:
        if char == 'O':
            amount_of_o += 1
        elif char == 'X':
            amount_of_x += 1
    if amount_of_x <= amount_of_o:
        return 'X'
    else:
        return 'O'


def is_table_filled(table):
    for cell in table:
        if cell in ['X', 'O']:
            pass
        else:
            return False
    return True


def check_position(initial_shape, position):
    is_user_input_valid = False
    is_type_ok = False
    try:
        pos_list = position.split()
        x = [int(pos_list[0]), int(pos_list[1])]
        is_type_ok = True
    except ValueError:
        print("You should enter numbers!")
    if is_type_ok:
        will_it_be_key_error = False
        if position.split()[0] not in ['1', '2', '3'] or position.split()[1] not in ['1', '2', '3']:
            print("Coordinates should be from 1 to 3!")
            will_it_be_key_error = True
        if not will_it_be_key_error:
            pos_list = position.split()
            position_as_string = ' '.join(pos_list)
            cell_value = add_spaces_to_initial_input(initial_shape)[convert_coordinates[position_as_string]]
            if cell_value in ['X', 'O']:
                print("This cell is occupied! Choose another one!")
            else:
                is_user_input_valid = True
    return is_user_input_valid


def check_win_condition(table):
    o_win = 'OOO'
    x_win = 'XXX'
    if table[:3] == o_win or table[3:6] == o_win or table[6:9] == o_win:
        return 'O'
    elif table[:3] == x_win or table[3:6] == x_win or table[6:9] == x_win:
        return 'X'
    elif table[:7:3] == o_win or table[1:8:3] == o_win or table[2:9:3] == o_win:
        return 'O'
    elif table[:7:3] == x_win or table[1:8:3] == x_win or table[2:9:3] == x_win:
        return 'X'
    elif table[0] + table[4] + table[8] == o_win:
        return 'O'
    elif table[0] + table[4] + table[8] == x_win:
        return 'X'
    elif table[2] + table[4] + table[6] == o_win:
        return 'O'
    elif table[2] + table[4] + table[6] == x_win:
        return 'X'
    else:
        return 'draw'


def get_check_mate_index(table):
    conditions = ['OO_', 'O_O', '_OO', 'XX_', 'X_X', '_XX']
    empty_index = {'OO_': 2, 'O_O': 1, '_OO': 0, 'XX_': 2, 'X_X': 1, '_XX': 0}
    for condition in conditions:
        if table[:3] == condition:
            return empty_index[condition]
        elif table[3:6] == condition:
            return 3 + empty_index[condition]
        elif table[6:9] == condition:
            return 6 + empty_index[condition]
        elif table[:7:3] == condition:
            return 3 * empty_index[condition]
        elif table[1:8:3] == condition:
            return 1 + 3 * empty_index[condition]
        elif table[2:9:3] == condition:
            return 2 + 3 * empty_index[condition]
        elif table[0] + table[4] + table[8] == condition:
            return 4 * empty_index[condition]
        elif table[2] + table[4] + table[6] == condition:
            return 2 + 2 * empty_index[condition]
    return None


def get_indexes_of_empty_cells(table_shape):
    indexes_of_empty_cells = []
    for char_index in range(len(table_shape)):
        if table_shape[char_index] == '_':
            indexes_of_empty_cells.append(char_index)
    return indexes_of_empty_cells


def get_random_position_index(indexes_of_empty_cells):
    return random.choice(indexes_of_empty_cells)


def get_state_of_the_game(table_shape):
    state = check_win_condition(table_shape)
    if is_table_filled(table_shape) and state == 'draw':
        return "Draw"
    elif state == 'X':
        return "X wins"
    elif state == 'O':
        return "O wins"
    else:
        return "Game not finished"


def is_input_command_valid(user_input_as_list):
    possible_first_arg = ['start', 'exit']
    possible_rest_of_args = ['easy', 'medium', 'hard', 'user']
    if len(user_input_as_list) == 1 and user_input_as_list[0] == 'exit':
        return True
    elif len(user_input_as_list) != 3:
        return False
    elif user_input_as_list[0] in possible_first_arg and user_input_as_list[1] in possible_rest_of_args and \
            user_input_as_list[2] in possible_rest_of_args:
        return True
    else:
        return False


# define minimax function
def minimax(table_state, ai_player):

    # declare opponent symbol
    if ai_player == 'X':
        opponent_symbol = 'O'
    else:
        opponent_symbol = 'X'

    # declare base conditions and assign score accordingly
    if check_win_condition(table_state) == ai_player:
        return {'score': 1 * (len(get_indexes_of_empty_cells(table_state)) + 1)}  # if AI wins
    elif check_win_condition(table_state) == opponent_symbol:
        return {'score': -1 * (len(get_indexes_of_empty_cells(table_state)) + 1)}  # if opponent wins
    elif is_table_filled(table_state):  # if its draw
        return {'score': 0}

    # list to store moves along with their scores
    moves = []

    # set proper symbol for this turn
    current_player_symbol = get_symbol_for_player(table_state)  # it will change state between X and O accordingly

    # get indexes of empty cells based on current table state
    possible_moves = get_indexes_of_empty_cells(table_state)

    # loop to make every possible move
    for move_index in possible_moves:

        # simulate a move by setting empty cell with current player symbol
        table_state = get_new_table_after_move(table_state, move_index, current_player_symbol)

        # make a dictionary to store index of current move and perform minimax function on new table
        move = {'index': move_index,
                'score': minimax(table_state, ai_player)['score']}

        # undo simulated move
        empty_symbol = '_'
        table_state = get_new_table_after_move(table_state, move_index, empty_symbol)

        # add move to a list in order to compare them later
        moves.append(move)

    # initiate dict
    best_move = {}

    # check if score should be max or min (depends on whose turn it is)
    if get_symbol_for_player(table_state) == ai_player:  # AI turn

        # set best score to -inf
        best_score = -math.inf

        # choose max score from moves
        for mov in moves:
            if mov['score'] > best_score:
                best_score = mov['score']
                best_move = mov

    else:  # opponents turn

        # set best score to +inf
        best_score = math.inf

        # choose min score from moves
        for mov in moves:
            if mov['score'] < best_score:
                best_score = mov['score']
                best_move = mov

    return best_move


def get_computer_move_index(table_shape, difficulty='easy'):
    if difficulty == 'easy':
        possible_moves = get_indexes_of_empty_cells(table_shape)
        chosen_computer_move = get_random_position_index(possible_moves)
        return chosen_computer_move
    elif difficulty == 'medium':
        check_mate_index = get_check_mate_index(table_shape)
        if check_mate_index is not None:
            return check_mate_index
        else:
            possible_moves = get_indexes_of_empty_cells(table_shape)
            chosen_computer_move = get_random_position_index(possible_moves)
            return chosen_computer_move
    elif difficulty == 'hard':
        chosen_computer_move = minimax(table_shape, get_symbol_for_player(table_shape))['index']
        return chosen_computer_move


class GameTable:

    def __init__(self, initial_shape):
        self.table_shape = initial_shape
        self.player_symbol = get_symbol_for_player(initial_shape)

    def display_table(self):
        shape_to_display = add_spaces_to_initial_input(self.table_shape)
        print("---------")
        print(("| " + shape_to_display[:5].replace('_', ' ') + " |"))
        print(("| " + shape_to_display[6:11].replace('_', ' ') + " |"))
        print(("| " + shape_to_display[12:17].replace('_', ' ') + " |"))
        print("---------")

    def user_request(self):
        process_finished = False
        while not process_finished:
            user_input_coordinates = input('Enter the coordinates:')
            if check_position(self.table_shape, user_input_coordinates):
                request_position = convert_coordinates_to_index[user_input_coordinates]
                list_of_table_shape = list(self.table_shape)
                list_of_table_shape[request_position] = get_symbol_for_player(self.table_shape)
                self.table_shape = ''.join(list_of_table_shape)
                process_finished = True

    def computer_request(self):
        computer_choice = get_computer_move_index(self.table_shape)
        list_of_table_shape = list(self.table_shape)
        list_of_table_shape[computer_choice] = 'O'
        self.table_shape = ''.join(list_of_table_shape)

    def make_move(self, set_player):
        if set_player == 'user':
            process_finished = False
            while not process_finished:
                user_input_coordinates = input('Enter the coordinates:')
                if check_position(self.table_shape, user_input_coordinates):
                    request_position = convert_coordinates_to_index[' '.join(user_input_coordinates.split())]
                    list_of_table_shape = list(self.table_shape)
                    list_of_table_shape[request_position] = get_symbol_for_player(self.table_shape)
                    self.table_shape = ''.join(list_of_table_shape)
                    process_finished = True
        elif set_player == 'easy':
            computer_choice = get_computer_move_index(self.table_shape, set_player)
            list_of_table_shape = list(self.table_shape)
            list_of_table_shape[computer_choice] = get_symbol_for_player(self.table_shape)
            self.table_shape = ''.join(list_of_table_shape)
            print('Making move level "easy"')
        elif set_player == 'medium':
            computer_choice = get_computer_move_index(self.table_shape, set_player)
            list_of_table_shape = list(self.table_shape)
            list_of_table_shape[computer_choice] = get_symbol_for_player(self.table_shape)
            self.table_shape = ''.join(list_of_table_shape)
            print('Making move level "medium"')
        elif set_player == 'hard':
            computer_choice = get_computer_move_index(self.table_shape, set_player)
            list_of_table_shape = list(self.table_shape)
            list_of_table_shape[computer_choice] = get_symbol_for_player(self.table_shape)
            self.table_shape = ''.join(list_of_table_shape)
            print('Making move level "hard"')


convert_coordinates = {'1 1': 0, '1 2': 2, '1 3': 4,
                       '2 1': 6, '2 2': 8, '2 3': 10,
                       '3 1': 12, '3 2': 14, '3 3': 16}

convert_coordinates_to_index = {'1 1': 0, '1 2': 1, '1 3': 2,
                                '2 1': 3, '2 2': 4, '2 3': 5,
                                '3 1': 6, '3 2': 7, '3 3': 8}

evaluation_of_state = {'X': {'X wins': 1,
                             'O wins': -1,
                             'Draw': 0},
                       'O': {'X wins': -1,
                             'O wins': 1,
                             'Draw': 0}}

if __name__ == '__main__':
    while 1:
        input_command = input("Input command: ").split()
        if is_input_command_valid(input_command):
            if input_command[0] == 'exit':
                sys.exit()
            else:
                tic_tac_toe = GameTable('_________')
                tic_tac_toe.display_table()
                player1 = input_command[1]
                player2 = input_command[2]
                should_player_move = True
            while get_state_of_the_game(tic_tac_toe.table_shape) == "Game not finished":
                tic_tac_toe.make_move(player1)
                tic_tac_toe.display_table()
                state_of_the_game = get_state_of_the_game(tic_tac_toe.table_shape)
                if state_of_the_game == 'Game not finished':
                    pass
                else:
                    print(state_of_the_game)
                    should_player_move = False
                if should_player_move:
                    tic_tac_toe.make_move(player2)
                    tic_tac_toe.display_table()
                    state_of_the_game = get_state_of_the_game(tic_tac_toe.table_shape)
                    if state_of_the_game == 'Game not finished':
                        pass
                    else:
                        print(state_of_the_game)
        else:
            print("Bad parameters!")

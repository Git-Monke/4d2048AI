from game import Board
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# number_of_state_checks = 100
simulations_per_state = 100
moves_per_simulation = 100000

action_types = [
    [Keys.ARROW_UP, Keys.ARROW_DOWN, Keys.ARROW_LEFT, Keys.ARROW_RIGHT],
    ["w", "s", "a", "d"],
]


def get_game_state(page_source):
    state = Board()
    soup = BeautifulSoup(page_source, "html.parser")
    tile_container = soup.find("div", class_="tile-container")

    for tile in tile_container.children:
        if tile.name is not None:
            class_names = tile.get("class", [])
            positions = list(map(lambda x: int(x) - 1, class_names[2][14:].split("-")))
            x, y = (
                positions[3] * 2 + positions[2],
                positions[1] * 2 + positions[0],
            )
            value = int(tile.find(class_="tile-inner").text)
            state.board[x][y] = value

    return state


def propogate_board(board, max_moves):
    moves = 0

    while not board.is_over and moves < max_moves:
        move_options = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
        success = False
        while success == False and len(move_options) > 0:
            move_index = random.randint(0, len(move_options) - 1)
            move_type, move_direction = move_options[move_index]
            move_options.pop(move_index)

            if move_type == 0:
                success = board.small_move(move_direction)
            else:
                success = board.large_move(move_direction)
        if len(move_options) == 0:
            break
        moves += 1

    return board.score(), moves


def score_state(board, move_type, move_direction, sim_count, moves_per_sim):
    sum_of_scores = 0
    sum_of_moves = 0
    print("Evaluating " + str(move_type) + " " + str(move_direction))
    for _ in range(sim_count):
        new_board = board.clone()
        if move_type == 0:
            board.small_move(move_direction)
        else:
            board.large_move(move_direction)
        score, moves = propogate_board(new_board, moves_per_sim)
        sum_of_scores += score
        sum_of_moves += moves

    print("Average value: " + str(sum_of_scores / sim_count))
    print("Average moves to termination: " + str(int(sum_of_moves / sim_count)))

    return sum_of_scores / sim_count


def choose_next_move(board):
    best_score = 0
    best_move_type, best_move_direction = 0, 0

    for i in [0, 1]:
        for x in range(4):
            clone = board.clone()
            tiles_moved = False
            if i == 0:
                tiles_moved = clone.small_move(x)
            else:
                tiles_moved = clone.large_move(x)
            if tiles_moved:
                score = score_state(
                    board.clone(), i, x, simulations_per_state, moves_per_simulation
                )
                if score > best_score:
                    best_score = score
                    best_move_type, best_move_direction = i, x

    print("Best move: " + str(best_move_type) + " " + str(best_move_direction))
    print(board.board)
    return best_move_type, best_move_direction


if __name__ == "__main__":
    print("Starting WebDriver")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://huonw.github.io/2048-4D/")

    actions = ActionChains(driver)

    while True:
        print("Parsing game state")
        board = get_game_state(driver.page_source)
        board.update_game_over_status()
        if board.is_over:
            print(board.board)
            break

        print("Choosing next move...")
        next_move_type, next_move_direction = choose_next_move(board)
        actions.send_keys(action_types[next_move_type][next_move_direction])
        actions.perform()
        time.sleep(0.1)

    # source = driver.page_source

    # board = get_game_state(source)

    # board.board[0][0] = 2
    # board.board[1][0] = 2

    # while not board.is_over:
    #     move_type, move_direction = choose_next_move(board)
    #     if move_type == 0:
    #         board.small_move(move_direction)
    #     else:
    #         board.large_move(move_direction)
    #     print(board.board)

    print("Game is over")
    input()
    driver.quit()

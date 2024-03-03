import numpy as np
import pygame
import math

game_over = False

row, col = 3, 3

gb = np.zeros((row, col))

turn = 1

window_width = window_height = 600

window_dimensions = (window_width, window_height)

window_bg_colour = (255, 255, 255)

window_line_colour = (0, 0, 0)

red = (255, 0, 0)

blue = (0, 0, 255)

circle = pygame.image.load('circle.png')

cross = pygame.image.load('x.png')


def draw_lines():
    pygame.draw.line(game_window, window_line_colour, (200, 0), (200, 600), 6)
    pygame.draw.line(game_window, window_line_colour, (400, 0), (400, 600), 6)
    pygame.draw.line(game_window, window_line_colour, (0, 200), (600, 200), 6)
    pygame.draw.line(game_window, window_line_colour, (0, 400), (600, 400), 6)


def draw_board():
    for c in range(col):
        for r in range(row):
            if gb[r][c] == 1:
                game_window.blit(cross, ((c*200)+50, (r*200)+50))
            elif gb[r][c] == 2:
                game_window.blit(circle, ((c * 200) + 50, (r * 200) + 50))
    pygame.display.update()


def game_window_reset():
    game_window.fill(window_bg_colour)
    draw_lines()
    pygame.display.update()


def player_move(current_row, current_col, current_pid):
    gb[current_row][current_col] = current_pid


def valid_move_check(check_row, check_col):
    return gb[check_row][check_col] == 0


def board_full_check(board_data):
    if 0 not in board_data:
        return True
    return False


def diag_check_down(r):
    count = {1: 0, 2: 0}
    for i in range(r):
        if gb[i][i] == 1:
            count[1] += 1
        elif gb[i][i] == 2:
            count[2] += 1
        else:
            return False
    if count[1] == 3:
        pygame.draw.line(game_window, red, (0, 0), (600, 600), 6)
        pygame.display.update()
        return 1
    elif count[2] == 3:
        pygame.draw.line(game_window, blue, (0, 0), (600, 600), 6)
        pygame.display.update()
        return 2


def diag_check_up(r):
    count = {1: 0, 2: 0}
    for i in range(r-1, -1, -1):
        if gb[i][r-1-i] == 1:
            count[1] += 1
        elif gb[i][r-1-i] == 2:
            count[2] += 1
        else:
            return False

    if count[1] == 3:
        pygame.draw.line(game_window, red, (0, 600), (600, 0), 8)
        pygame.display.update()
        return 1
    elif count[2] == 3:
        pygame.draw.line(game_window, blue, (0, 600), (600, 0), 8)
        pygame.display.update()
        return 2


def row_check(r):
    for r_no in range(r):
        if all(x == 1 for x in gb[r_no]):
            pygame.draw.line(game_window, red, (10, (r_no*200)+100), (window_width - 10, (r_no*200)+100), 6)
            pygame.display.update()
            return 1
        elif all(x == 2 for x in gb[r_no]):
            pygame.draw.line(game_window, blue, (10, (r_no * 200) + 100), (window_width - 10, (r_no * 200) + 100), 6)
            pygame.display.update()
            return 2
    return False


def col_check(c):
    for c_no in range(c):
        v_count = {1: 0, 2: 0}
        for r_no in range(c):
            if gb[r_no][c_no] == 1:
                v_count[1] += 1
            elif gb[r_no][c_no] == 2:
                v_count[2] += 1
        if v_count[1] == 3:
            pygame.draw.line(game_window, red, ((c_no * 200) + 100, 10), ((c_no * 200) + 100, window_height - 10), 6)
            pygame.display.update()
            return 1
        elif v_count[2] == 3:
            pygame.draw.line(game_window, blue, ((c_no * 200) + 100, 10), ((c_no * 200) + 100, window_height - 10), 6)
            pygame.display.update()
            return 2
    return False


def game_won(r, c):
    winner = ''
    winner_by_row = row_check(r)
    winner_by_col = col_check(c)
    winner_diag_up = diag_check_up(r=row)
    winner_diag_down = diag_check_down(r=row)
    p1 = ((winner_by_row == 1) or (winner_diag_up == 1) or (winner_diag_down == 1) or (winner_by_col == 1))
    p2 = ((winner_by_row == 2) or (winner_diag_up == 2) or (winner_diag_down == 2) or (winner_by_col == 2))

    if p1:
        winner = 'Player 1'

    elif p2:
        winner = 'Player 2'

    if winner:
        print(f'{winner} has won the game!')
        return True

    return False


pygame.init()
game_window = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption("Tic-Tac-Toe")
game_window.fill(window_bg_colour)
draw_lines()
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

            pid = turn % 2
            if pid == 0:
                p = 2
            else:
                p = 1

            r, c = math.floor(event.pos[1]/200), math.floor(event.pos[0]/200)

            if valid_move_check(r, c):
                print("valid move.")
                player_move(r, c, p)
            else:
                print("Not a valid move.")
                turn -= 1
            print(gb)
            draw_board()
            turn += 1
    if board_full_check(gb) or game_won(row, col):
        print("Game Over. RESET....")
        gb = np.zeros((row, col))
        pygame.time.wait(500)
        game_window_reset()
        turn = 1

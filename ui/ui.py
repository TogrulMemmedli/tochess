import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import chess
import time

from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent

WIDTH, HEIGHT = 400, 400
DIMENSION = 8  
SQ_SIZE = HEIGHT // DIMENSION
COLORS = [pygame.Color("white"), pygame.Color("black")] 
IMAGES = {}

WHITE_PLAYER = RandomAgent()
BLACK_PLAYER = GreedyAgent() 

def load_images():
    pieces = ['wp', 'wr', 'wk', 'wb', 'wK', 'wq', 'bp', 'br', 'bk', 'bb', 'bK', 'bq']
    pieces_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "pieces")
    for piece in pieces:
        filename = piece if piece in ['wK', 'bK'] else piece.lower()
        image_path = os.path.join(pieces_folder, f"{filename}.png")
        try:
            image = pygame.image.load(image_path)
            IMAGES[piece] = pygame.transform.smoothscale(image, (int(SQ_SIZE * 0.95), int(SQ_SIZE * 0.95)))
        except pygame.error as e:
            print(f"Error: {image_path} not found. {e}")

def draw_board(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = COLORS[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_highlights(screen, board, sq_selected, human_turn):
    if human_turn and sq_selected != ():
        r, c = sq_selected
        from_square = chess.square(c, 7 - r)
        piece = board.piece_at(from_square)
        
        if piece and piece.color == board.turn:
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) 
            s.fill(pygame.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            
            legal_moves = [move for move in board.legal_moves if move.from_square == from_square]
            for move in legal_moves:
                to_r = 7 - chess.square_rank(move.to_square)
                to_c = chess.square_file(move.to_square)
                
                circle_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (0, 150, 0, 120), (SQ_SIZE // 2, SQ_SIZE // 2), SQ_SIZE // 6)
                screen.blit(circle_surface, (to_c * SQ_SIZE, to_r * SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                symbol = piece.symbol()
                color_prefix = 'w' if piece.color == chess.WHITE else 'b'
                piece_type = symbol.lower() if symbol.lower() != 'n' else 'k'
                if symbol.upper() == 'K': piece_type = 'K'
                img_key = f"{color_prefix}{piece_type}"
                
                offset = (SQ_SIZE - int(SQ_SIZE * 0.95)) // 2
                screen.blit(IMAGES[img_key], pygame.Rect(c*SQ_SIZE + offset, r*SQ_SIZE + offset, SQ_SIZE, SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("tochess UI v0.1.0")
    load_images()
    
    board = chess.Board() 
    sq_selected = () 
    player_clicks = [] 
    game_over = False
    
    running = True
    while running:
        human_turn = (board.turn == chess.WHITE and WHITE_PLAYER == 'human') or \
                     (board.turn == chess.BLACK and BLACK_PLAYER == 'human')

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            elif not game_over and human_turn and e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                
                if sq_selected == (row, col): 
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                
                if len(player_clicks) == 2:
                    r1, c1 = player_clicks[0]
                    r2, c2 = player_clicks[1]
                    from_sq = chess.square(c1, 7 - r1)
                    to_sq = chess.square(c2, 7 - r2)
                    
                    piece = board.piece_at(from_sq)
                    
                    if piece and piece.color == board.turn:
                        is_promotion = False
                        if piece.piece_type == chess.PAWN:
                            if (piece.color == chess.WHITE and r2 == 0) or (piece.color == chess.BLACK and r2 == 7):
                                is_promotion = True

                        move = None
                        if is_promotion:
                            print("Promotion! Q (Queen), N (Knight), R (Rook), B (Bishop) select")
                            waiting_for_input = True
                            while waiting_for_input:
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_q: move = chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
                                        elif event.key == pygame.K_n: move = chess.Move(from_sq, to_sq, promotion=chess.KNIGHT)
                                        elif event.key == pygame.K_r: move = chess.Move(from_sq, to_sq, promotion=chess.ROOK)
                                        elif event.key == pygame.K_b: move = chess.Move(from_sq, to_sq, promotion=chess.BISHOP)
                                        
                                        if move: waiting_for_input = False
                                    elif event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                        else:
                            move = chess.Move(from_sq, to_sq)

                        if move in board.legal_moves:
                            board.push(move)
                            sq_selected = ()
                            player_clicks = []
                        else:
                            sq_selected = (row, col)
                            player_clicks = [sq_selected]
                    else:
                        sq_selected = (row, col)
                        player_clicks = [sq_selected]

        if not game_over and not human_turn:
            current_agent = WHITE_PLAYER if board.turn == chess.WHITE else BLACK_PLAYER
            
            if current_agent != 'human':
                pygame.display.flip()
                time.sleep(0.1) 
                
                move = current_agent.get_move(board)
                if move:
                    board.push(move)
                    print(f"{current_agent.name} moved: {move.uci()}")

        if board.is_game_over() and not game_over:
            game_over = True
            print("Game Over!")
            print("Result:", board.result())

        draw_board(screen)
        draw_highlights(screen, board, sq_selected, human_turn)
        draw_pieces(screen, board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
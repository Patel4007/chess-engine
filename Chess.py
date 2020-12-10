import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def findMoveMinMax(game_state, valid_moves, return_queue):
    global next_move
    turn_multiplier = 1 if game_state.white_to_move else -1
    opponentMinMaxScore = CHECKMATE

    next_move = None
    random.shuffle(valid_moves)

    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)

    for move in valid_moves:
        game_state.makeMove(move)

        opponentsMoves = game_state.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            game_state.makeMove(opponentsMove)
            if game_state.checkmate:
                score = -turn_multiplier * CHECKMATE
            elif game_state.stalemate:
                score = 0
            else:
                score = turn_multiplier * scoreBoard(game_state)
            if score > opponentMaxScore:
                opponentMaxScore = score
            game_state.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def scoreBoard(game_state):

    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                if piece[0] == "w":
                    score += piece_score[piece[1]]
                if piece[0] == "b":
                    score -= piece_score[piece[1]]

    return score


def findRandomMove(valid_moves):

    return random.choice(valid_moves)
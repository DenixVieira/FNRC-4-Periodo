''' Esse é o arquivo principal, ele será responsável por receber os comandos no display que ocorrer durante o jogo '''
import ChessEngine
import pygame as p
import math

# kassio
width = height = 512
dim = 8  # Dimensões (8x8)
sqsize = height // dim
maxfps = 15
images = {}

'''
Para melhor desempenho, é necessário que as imagens sejam alocadas na memória apenas uma vez no arquivo principal
'''


def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ",
              "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load(
            "images/" + piece + ".png"), (sqsize, sqsize))
        # 'transform.scale' está redimencionando a imagem mantendo a qualidade passando o parâmetro do tamanho que é N²


'''
O arquivo principal do projeto, ele irá dar conta da rederização e atualização das imagens
'''


def main():
    p.init()
    screen = p.display.set_mode((width, height))  # Criando a tela do jogo
    clock = p.time.Clock()  # Relógio do jogo
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variavel para quando um movimento é feito
    loadImages()  # As imagens é chamada apenas uma vez antes do loop
    running = True  # condição para o loop da tela
    sqSelected = ()  # Armazena a casa que o usuário clicar, (Tupla: (linha, coluna))
    # mantem armazenado os clicks do usuário (duas tulplas: [(6,4),(4,4)])
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # Evento de sair
                running = False

            # manipulando mouse
            elif e.type == p.MOUSEBUTTONDOWN:  # Evento de click do mouse
                location = p.mouse.get_pos()  # captura a posição do mouse
                col = location[0]//sqsize
                row = location[1]//sqsize
                if sqSelected == (row, col):  # o usuário clickou nas mesmas casas
                    sqSelected = ()
                    playerClicks = []  # retira o click do player
                else:
                    sqSelected = (row, col)
                    # Adicionando o primeiro e segundo click do usuário
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:  # depois do segundo click
                    move = ChessEngine.Move(
                        playerClicks[0], playerClicks[1], gs.board)

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reseta a seleção
                        playerClicks = []  # resetando os clicks
                    else:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # defaz quando a tecla "z" é pressionada
                    gs.undoMove()
                    sqSelected = ()  # reseta a seleção
                    playerClicks = []  # resetando os clicks
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(maxfps)
        p.display.flip()


'''
Responsável por todos os desenhos com e interações
'''


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


'''
 Desenha as casas na tábua
'''


def drawBoard(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(dim):
        for c in range(dim):
            '''
            levando em consideração que o r(linha) na posição 0 e o r na posição 1 irão dar restos diferentes quando forem 
            comparado com o c(coluna) na posição zero por exemplo. Então abaixo temos a seleção das cores mediante o que for o 
            resultado do resto
            '''
            colour = colours[((r + c) % 2)]
            p.draw.rect(screen, colour, p.Rect(
                c*sqsize, r*sqsize, sqsize, sqsize))


'''
desenha as peças em cima das casas
'''


def drawPieces(screen, board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":  # casa não Não está vazia
                screen.blit(images[piece], p.Rect(
                    c*sqsize, r*sqsize, sqsize, sqsize))


if __name__ == "__main__":
    main()

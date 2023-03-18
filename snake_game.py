import pygame
import random
pygame.init()

# Configurações do jogo
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SNAKE_SIZE = 20
SNAKE_SPEED = 15

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#Configurações para tela inicial
def draw_start_screen(screen):
    screen.fill(WHITE)  

    font = pygame.font.Font(None, 36)
    text = font.render("Bem-vindo ao SNAKE GAME!", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height()))

    font = pygame.font.Font(None, 24)
    text = font.render("Pressione qualquer tecla para começar", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height()))

#Configurações de pontuação
def draw_score(screen, score):
    font = pygame.font.Font(None, 24)
    text = font.render(f"Pontuação: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

#Configurações para tela game over
def draw_game_over_screen(screen, score):
    screen.fill(WHITE)

    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3 - text.get_height()))

    font = pygame.font.Font(None, 24)
    text = font.render(f"Pontuação: {score}", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height()))

    font = pygame.font.Font(None, 24)
    text = font.render("Pressione 'R' para jogar novamente ou 'ESC' para sair", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height()))    

#Configurações para criação da cobrinha
def create_snake():
    x = (SCREEN_WIDTH // 2) // SNAKE_SIZE * SNAKE_SIZE
    y = (SCREEN_HEIGHT // 2) // SNAKE_SIZE * SNAKE_SIZE
    return [(x, y), (x - SNAKE_SIZE, y), (x - (2 * SNAKE_SIZE), y)]

#Configurações para geração de comida
def create_food(snake):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        if (x, y) not in snake:
            return (x, y)

#Configurações para a posições dos objetos em tela
def draw_objects(screen, snake, food):
    screen.fill(WHITE)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))

#Configurações do jogo
def main():

    # Crie a janela do jogo e defina o título
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Controle a velocidade do jogo
    clock = pygame.time.Clock()

    # Adicione esta parte para exibir a tela de início
    draw_start_screen(screen)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                waiting = False

    # Inicialize a cobrinha e a comida
    snake = create_snake()
    food = create_food(snake)

    # Variáveis para armazenar a direção atual e a próxima direção da cobrinha
    direction = pygame.K_RIGHT
    next_direction = direction

    # Inicialize a pontuação
    score = 0

    running = True
    while running:
        # Verifique se algum evento ocorreu, como pressionar uma tecla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    next_direction = event.key

        # Verifique se a próxima direção é válida e atualize a direção atual
        if (
            next_direction == pygame.K_UP and direction != pygame.K_DOWN
            or next_direction == pygame.K_DOWN and direction != pygame.K_UP
            or next_direction == pygame.K_LEFT and direction != pygame.K_RIGHT
            or next_direction == pygame.K_RIGHT and direction != pygame.K_LEFT
        ):
            direction = next_direction

        # Mova a cobrinha na direção atual
        dx, dy = 0, 0
        if direction == pygame.K_UP:
            dy = -SNAKE_SIZE
        elif direction == pygame.K_DOWN:
            dy = SNAKE_SIZE
        elif direction == pygame.K_LEFT:
            dx = -SNAKE_SIZE
        elif direction == pygame.K_RIGHT:
            dx = SNAKE_SIZE

        new_head = ((snake[0][0] + dx) % SCREEN_WIDTH, (snake[0][1] + dy) % SCREEN_HEIGHT)

        # Verifique se a cobrinha colidiu consigo mesma
        if (
            
            new_head in snake

        ):
            running = False

            # Exiba a tela de "Game Over"
            draw_game_over_screen(screen, score)
            pygame.display.flip()

            # Aguarde o jogador pressionar uma tecla
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            waiting = False
                            main()  # Reinicie o jogo chamando a função `main()` novamente
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return

        # Atualize a posição da cobrinha
        snake.insert(0, new_head)

        # Verifique se a cobrinha comeu a comida e atualize sua posição
        if new_head == food:
            food = create_food(snake)
            score += 1  # Atualize a pontuação
        else:
            snake.pop()

        # Desenhe a cobrinha e a comida na tela
        draw_objects(screen, snake, food)
        draw_score(screen, score) 
        pygame.display.flip()

        # Controle a velocidade do jogo
        clock.tick(SNAKE_SPEED)

    pygame.quit()

if __name__ == "__main__":
    main()
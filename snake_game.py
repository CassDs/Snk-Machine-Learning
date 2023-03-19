import pygame
import random
pygame.init()

# Configurações do jogo
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SNAKE_SIZE = 20
SNAKE_SPEED = 15
LEVEL_UP_SCORE = 5


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

#Configuração de dificuldade do jogo

def draw_level(screen, level):
    rounded_level = round(level)  
    font = pygame.font.Font(None, 24)
    text = font.render(f"Nível: {rounded_level}", True, (0, 0, 0))  
    screen.blit(text, (SCREEN_WIDTH - 100, 10))

#Ler a pontuação mais alta
def read_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except (FileNotFoundError, ValueError):
        high_score = 0
    return high_score

#Salva a pontuação mais alta
def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

#Exibe pontuação mais alta em tela
def draw_high_score(screen, high_score):
    font = pygame.font.Font(None, 24)
    text = font.render(f"Pontuação mais alta: {high_score}", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH - 250, 10))


#Configurações do jogo
def main():
    # Configura a tela do jogo e define o título
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Configura o relógio para controlar a velocidade do jogo
    clock = pygame.time.Clock()

    # Exibe a tela de início e aguarda o jogador pressionar uma tecla
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

    # Inicializa a cobra e a comida
    snake = create_snake()
    food = create_food(snake)

    # Define a direção inicial da cobra e a próxima direção
    direction = pygame.K_RIGHT
    next_direction = direction

    # Inicializa a pontuação e o nível do jogo
    score = 0
    level = 1

    # Lê a pontuação mais alta salva
    high_score = read_high_score()

    # Inicia o loop principal do jogo
    running = True
    while running:
        # Verifica se algum evento ocorreu, como pressionar uma tecla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    next_direction = event.key

        # Atualiza a direção da cobra, se a próxima direção for válida
        if (
            next_direction == pygame.K_UP and direction != pygame.K_DOWN
            or next_direction == pygame.K_DOWN and direction != pygame.K_UP
            or next_direction == pygame.K_LEFT and direction != pygame.K_RIGHT
            or next_direction == pygame.K_RIGHT and direction != pygame.K_LEFT
        ):
            direction = next_direction

        # Atualiza a posição da cobra com base na direção atual
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

        # Verifica se a cobra colidiu consigo mesma e encerra o jogo, se necessário
        if new_head in snake:
            running = False

        # Insere a nova posição da cabeça da cobra
        snake.insert(0, new_head)

        # Verifica se a cobra comeu a comida e atualiza sua posição
        if new_head == food:
            food = create_food(snake)
            score += 1  # Atualiza a pontuação

            # Verifica se o jogador atingiu o próximo nível
            if score % LEVEL_UP_SCORE == 0:
                level += 0.1
        else:
            # Remove o último segmento da cobra, caso não tenha comido a comida
            snake.pop()

        # Desenha a cobra, a comida, a pontuação e o nível na tela
        draw_objects(screen, snake, food)
        draw_score(screen, score)
        draw_level(screen, level)
        pygame.display.flip()

        # Atualiza a velocidade da cobra com base no nível atual
        clock.tick(SNAKE_SPEED * level)

    # O jogo terminou, então verifique se a pontuação atual é maior que a pontuação mais alta e salve, se necessário
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Exibe a tela de "Game Over" e aguarda o jogador pressionar uma tecla
    draw_game_over_screen(screen, score)
    pygame.display.flip()

    draw_high_score(screen, high_score)
    pygame.display.flip()

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

    pygame.quit()

if __name__ == "__main__":
    main()


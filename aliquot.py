import pygame
import sys
import math

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

BLACK = (0, 0, 0)
AMBER = (255, 191, 0)

font = pygame.font.Font(None, 36)
computed_sequences = {}

def divisor_sum(n):
    if n == 1:
        return 0
    divisors_sum = 1
    sqrt_n = int(math.sqrt(n))
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            divisors_sum += i
            if i != n // i:  
                divisors_sum += n // i
    return divisors_sum


def aliquot_sequence(n, max_length):
    sequence = [n]
    computed = {n}
    current = n
    while len(sequence) < max_length:
        next_num = divisor_sum(current)
        sequence.append(next_num)
        computed.add(next_num)
        current = next_num
    return sequence

def get_or_calculate_sequence(number, max_len):
    if number not in computed_sequences:
        computed_sequences[number] = aliquot_sequence(number, max_len)
    return computed_sequences[number]

def draw_line(screen, sequence, index, scale_x, max_value):
    if index < len(sequence) - 1:
        line_color = AMBER
        if sequence[index] <= 0 or sequence[index + 1] <= 0:
            y1 = screen_height - 25
            y2 = screen_height - 25
        else:
            y1 = screen_height - math.log(sequence[index]) * (
                screen_height - 50
            ) / math.log(max_value)
            y2 = screen_height - math.log(sequence[index + 1]) * (
                screen_height - 50
            ) / math.log(max_value)
        pygame.draw.line(
            screen, line_color, (index * scale_x, y1), ((index + 1) * scale_x, y2), 2
        )
        

def main():
    max_len=40
    maxxx = 0
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Aliquot Sequence Chart")
    crt_overlay = pygame.image.load("Perfect_CRT.png").convert_alpha()
    crt_overlay = pygame.transform.scale(crt_overlay, (screen_width, screen_height))
    running = True
    n = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

        if not running:
            pygame.quit()
            sys.exit()

        maxxx = max(draw_sequences(screen, n, max_len), maxxx)

        number_text = font.render(
            f"Number: {n}     Max Value Reached: {maxxx}    Maximum Steps:  {max_len}", True, AMBER
        )
        screen.blit(number_text, (20, 20))
        screen.blit(crt_overlay, (0, 0))
        pygame.display.flip()

        n += 1
        
        pygame.time.delay(100)
        


def draw_sequences(screen, current_number, max_len):
    screen.fill(BLACK)
    max_value = 1  
    scale_x = screen_width // max_len

    for num in range(1, current_number):
        seq = get_or_calculate_sequence(num, max_len)
        max_value = max(max_value, max(seq))

    for num in range(1, current_number):
        sequence = get_or_calculate_sequence(num, max_len)
        for i in range(len(sequence) - 1):
            draw_line(screen, sequence, i, scale_x, max_value)

    return max_value

if __name__ == "__main__":
    main()

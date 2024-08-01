import pygame
import requests
import json

WEBHOOK_URL = "..."
WIDTH, HEIGHT = 600, 400
sent_messages = []

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)

def send_discord_message(message):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        sent_messages.append(message)

def main():
    input_box = pygame.Rect(50, 100, 500, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                    color = color_active if active else color_inactive

                for index in range(len(sent_messages)):
                    message_rect = pygame.Rect(50, 160 + index * 30, 500, 30)
                    if message_rect.collidepoint(event.pos):
                        del sent_messages[index]
                        break

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        send_discord_message(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        for index, message in enumerate(sent_messages):
            message_surface = font.render(f"{index + 1}: {message}", True, (255, 255, 255))
            screen.blit(message_surface, (50, 160 + index * 30))

        txt_surface = font.render(text, True, color)
        width = max(500, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

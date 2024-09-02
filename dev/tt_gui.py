import pygame


def main():
    screen = pygame.display.set_mode((640, 480))
    width = screen.get_width()
    height = screen.get_height()
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(215, height / 2, 140, 32)
    refresh_box = pygame.Rect(width / 5, height / 5, 140, 140)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            """
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            """
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if user clicks refresh button
                if refresh_box.collidepoint(event.pos):
                    print("refreshed")
                else:
                    active = False
                color = color_active if active else color_inactive

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        refresh_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (refresh_box.x+5, refresh_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, refresh_box, 2)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
import sys
import pygame

class GameLoop(object):
    def __init__(self, handler):
        self.handler = handler

    def run(self):
        size = width, height = 700, 700
        black = 0, 0, 0

        screen = pygame.display.set_mode(size)
        pygame.time.set_timer(pygame.USEREVENT, 16)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.USEREVENT:
                    self.handle_transition(self.handler.handle_tick())
                else:
                    self.handle_transition(self.handler.handle_event(event))

            screen.fill((255, 255, 255))

            self.handler.draw(screen)

            pygame.display.flip()

            clock.tick(50)

    def handle_transition(self, next_handler):
        if next_handler:
            self.handler = next_handler

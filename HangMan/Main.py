import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("HangMan")

images = []
for i in range(7):
    image = pygame.image.load("hangman" +str(i)+".png" )
    images.append(image)
GAP = 15
RADIUS = 20
letters = []
startx = round((WIDTH - (RADIUS *2) * 13)/2)-70
starty = 400
for i in range(26):
    x = startx +  ((RADIUS *2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x,y, chr(65+i), True])
    
hangman_status = 0
word = "DEVELOPMENT"
guess = []
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 60
LETTER_FONT = pygame.font.SysFont('comicsans', 35)
clock = pygame.time.Clock()
def draw():
    win.fill(WHITE)
    Dword = ""
    for w in word:
        if w in guess:
            Dword += w + ' '
        else:
            Dword += '_ '

    text = LETTER_FONT.render(Dword,1,BLACK)
    win.blit(text,(400,200))
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x,y), RADIUS, 3)
            text = LETTER_FONT.render(ltr,1,BLACK)
            win.blit(text, (x- text.get_width()/2,y- text.get_height()/2))
    
    win.blit(images[hangman_status],(150,100))
    pygame.display.update()
run = True

while run:
    clock.tick(FPS)

    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for letter in letters:
                x,y,ltr, visible = letter
                if visible:
                    dis = math.sqrt((x-mx)**2+(y-my)**2)
                    if dis<RADIUS:
                        letter[3] = False
                        guess.append(ltr)
                        if ltr not in word:
                            hangman_status +=1

    won = True
    for letter in word:
        if letter not in guess:
            won = False
            break

    if won:
        print("You Won The Game")
        break

    if hangman_status == 6:
        print("You Lost The Game")
        break
                    

pygame.quit()

import pygame, random, os
pygame.init()


class matching_aliens():


    def __init__(self):
        ##fourth step 
        # all about music 
        self.music_playing = True
        self.speaker  = pygame.image.load('F:\match aliens\speaker.png').convert_alpha()
        self.scaled_speaker = pygame.transform.scale(self.speaker , (30,30))
        self.pause= pygame.image.load('F:\match aliens\pausee.png').convert_alpha()
        self.scaled_pause  = pygame.transform.scale(self.pause, (30,30))
        self.music = self.scaled_speaker
        self.music_rect = self.music.get_rect(topright = (width- 10, 10))
        
        pygame.mixer.music.load('F:\match aliens\cyber-attack-dark-epic-and-mystically-music-7594.mp3')
        pygame.mixer.music.play()
        


        self.level = 1
        self.level_complete = False

        # aliens
        self.all_aliens = [f for f in os.listdir('images/aliens') if os.path.join('images/aliens', f)]
        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1200
        self.blocks_group = pygame.sprite.Group()
        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False
        # generate first level
        self.generate_level(self.level)


    ###third step write on screen 
    def on_screen(self):
        # 1 Game font 
        self.title_font = pygame.font.Font('F:\match aliens\Little Alien.ttf', 50)
        self.other_font = pygame.font.Font('F:\match aliens\Little Alien.ttf',26)
        # 2 Game text 
        self.title_text = self.title_font.render('Match Aliens ', True,(255,255,255))
        self.title_rect = self.title_text.get_rect(midtop = (width  // 2, 10))
        self.level_text = self.other_font.render('Level ' + str(self.level), True,(255,255,255))
        self.level_rect = self.level_text.get_rect(midtop = (width// 2, 80))
        #3 blit 
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.level_text, self.level_rect)
        screen.blit(self.music, self.music_rect)
        #4 message by each level 
        if  self.level != 5:
            self.next_text = self.other_font.render('Level complete. Press Space for next level', True,(255,255,255))
        else:
            self.next_text = self.other_font.render('levels complete, Press Space to play again', True, (255,255,255))
        self.next_rect = self.next_text.get_rect(midbottom = (width// 2, hieght - 40))
         

        
        
        # draw tileset
        self.blocks_group.draw(screen)
        self.blocks_group.update()

        if self.level_complete:
            screen.blit(self.next_text, self.next_rect)

    
    def Game_event(self, each_event):
        #fifth 
        for event in each_event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.music_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.music_playing:
                        self.music_playing = False
                        self.music= self.scaled_pause
                        pygame.mixer.music.pause()
                    else:
                        self.music_playing = True
                        self.music = self.scaled_speaker
                        pygame.mixer.music.unpause()
            # k and n 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 6:
                        self.level = 1
                    self.generate_level(self.level)

    #n and k 
    def check_level_complete(self, each_event ):
        if not self.block_game:
            for event in each_event :
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.blocks_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.blocks_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == Frames_per_second:
                self.frame_count = 0
                self.block_game = False

                for tile in self.blocks_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []


    def generate_level(self, level):
        self.aliens = self.select_random_aliens(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.aliens)

    def generate_tileset(self, aliens):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARING = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        self.blocks_group.empty()

        for i in range(len(aliens)):
            x = LEFT_MARING + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(aliens[i], x, y)
            self.blocks_group.add(tile)


    def select_random_aliens(self, level):
        aliens = random.sample(self.all_aliens, (self.level + self.level + 2))
        aliens_copy = aliens.copy()
        aliens.extend(aliens_copy)
        random.shuffle(aliens)
        return aliens
  

   # n 
  


    def update(self,each_event ):
        self.Game_event(each_event )
        self.on_screen()
        self.check_level_complete(each_event)


    
class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('images/aliens/' + filename)

        self.back_image = pygame.image.load('images/aliens/' + filename)
        pygame.draw.rect(self.back_image, (255,255,255), self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True
    def hide(self):
        self.shown = False

    


#first step:  size and background 
width  = 1200
hieght = 800
screen = pygame.display.set_mode( (width,hieght))
background_image=pygame.image.load("F:\match aliens\khadija.jpg")
scaled_back_ground = pygame.transform.scale(background_image , (width ,hieght))


# second step: game caption and icon 
pygame.display.set_caption('Match Aliens')
pygame.display.set_icon(pygame.image.load('F:\match aliens\e.png'))


Frames_per_second = 45
clock = pygame.time.Clock()

#instantiationn..0.0...
game = matching_aliens()

#third step: game loop 
running = True
while running:
    screen.fill((255,255, 255))   # RGB
    screen.blit(scaled_back_ground , (0,0))

    each_event  = pygame.event.get()
    for event in each_event  :
        if event.type == pygame.QUIT:
            running = False

    game.update(each_event )

    pygame.display.update()
    clock.tick(Frames_per_second)


pygame.quit()

import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group) -> None:
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
    
    def use_tool(self):
        # print(self.selected_tool)
        pass

    def use_seed(self):
        # print(self.selected_seed)
        pass

    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
                           'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

        for animation in self.animations.keys():
            full_path = 'graphics\\character\\' + animation
            self.animations[animation] = import_folder(full_path)
        # print(self.animations)

    def animate(self, dt):
        self.frame_index += 4*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
            # directions
            if keys[pygame.K_UP]:
                # print("up pressed")
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                # print("down pressed")
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                # print("right pressed")
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                # print("left pressed")
                self.direction.x = -1
                self.status = 'left'
            
            else:
                self.direction.x = 0
        
            # tool use
            if keys[pygame.K_SPACE]:
                # timer for tool use
                self.timers['tool use'].activate() 
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # change tool 
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                if self.tool_index < len(self.tools) - 1:
                    self.tool_index += 1
                else:
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]
            
            # seed use
            if keys[pygame.K_LCTRL]:
                # timer for seed use
                self.timers['seed use'].activate() 
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                print("use seed")

            # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                if self.seed_index < len(self.seeds) - 1:
                    self.seed_index += 1
                else:
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]
                print(self.selected_seed)
    
    def get_status(self):
        
        # check if player is not moving(idle) add _idle to its current status
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + "_idle"
        
        if self.timers['tool use'].active:
            # print("using tool")
            self.status = self.status.split('_')[0] + "_" + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):

        # normalize a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # print(self.direction)
        
        # horizontal movement 
        self.pos.x += self.direction.x*self.speed*dt
        self.rect.centerx = self.pos.x

        # vertical movement 
        self.pos.y += self.direction.y*self.speed*dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)



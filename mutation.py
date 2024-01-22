# class Mutations(pygame.sprite.Sprite):
#     def __init__(self):
#         double_shot = pygame.image.load("graphics/double_shot.png").convert_alpha()
#         double_shot = pygame.transform.scale_by(double_shot, 5)
#         double_shot_font = mutation_font.render("Double Shot",False,"black")
#         poison_shot = pygame.image.load("graphics/poison_shot.png").convert_alpha()
#         poison_shot = pygame.transform.scale_by(poison_shot, 5)
#         poison_shot_font = mutation_font.render("Poison Shot",False,"black")
#         flank_shot = pygame.image.load("graphics/flank_shot.png").convert_alpha()
#         flank_shot = pygame.transform.scale_by(flank_shot, 5)
#         flank_shot_font = mutation_font.render("Flank Shot",False,"black")

#         self.mutations = {}
#         self.mutations[double_shot] = double_shot_font
#         self.mutations[poison_shot] = poison_shot_font
#         self.mutations[flank_shot] = flank_shot_font

#         self.image = pygame.image.load("graphics/mutation_card.png").convert_alpha()
#         self.image = pygame.transform.scale_by(self.image, 15)
#         self.rect = self.image.get_rect(center = (850,450))
#         self.mutation_list = [double_shot,poison_shot,flank_shot]
#         self.mutation_list_num = [0,1,2]
#         self.not_chosen = True

#     def pick_three(self):
#         if self.not_chosen:
#             random.shuffle(self.mutation_list_num)
#             self.not_chosen = False

#     def display_mutations(self):
#         self.rect = self.image.get_rect(center = (850,450))
#         screen.blit(self.image,self.rect)
#         self.rect = self.image.get_rect(center = (1250,450))
#         screen.blit(self.image,self.rect)
#         self.rect = self.image.get_rect(center = (450,450))
#         screen.blit(self.image,self.rect)

#         self.rect = self.image.get_rect(center = (614,525))
#         screen.blit(self.mutation_list[self.mutation_list_num[0]],self.rect)
#         self.rect = self.image.get_rect(midleft = (344,685))
#         screen.blit(self.mutations.get(self.mutation_list[0]),self.rect)

#         self.rect = self.image.get_rect(center = (1014,525))
#         screen.blit(self.mutation_list[self.mutation_list_num[1]],self.rect)
#         self.rect = self.image.get_rect(midleft = (749,685))
#         screen.blit(self.mutations.get(self.mutation_list[1]),self.rect)

#         self.rect = self.image.get_rect(center = (1414,525))
#         screen.blit(self.mutation_list[self.mutation_list_num[2]],self.rect)
#         self.rect = self.image.get_rect(midleft = (1150,685))
#         screen.blit(self.mutations.get(self.mutation_list[2]),self.rect)

#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_1]:
#             ship.activate_mutation(self.mutation_list_num[0])
#             self.mutation_list_num.pop(0)
#             self.not_chosen = True
#             return False
#         if keys[pygame.K_2]:
#             ship.activate_mutation(self.mutation_list_num[1])
#             self.mutation_list_num.pop(1)
#             self.not_chosen = True
#             return False
#         if keys[pygame.K_3]:
#             ship.activate_mutation(self.mutation_list_num[2])
#             self.mutation_list_num.pop(2)
#             self.not_chosen = True
#             return False
        
#         return True
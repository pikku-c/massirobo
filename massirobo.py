import pygame
from random import randint

class Peli:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Massirobo")
        self.leveys = 720   
        self.korkeus = 520
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.robo = pygame.image.load("robo.png")
        self.pahis = pygame.image.load("hirvio.png")
        self.kolikko = pygame.image.load("kolikko.png")
        self.roboleveys = self.robo.get_width()
        self.robokorkeus = self.robo.get_height()
        self.pahis_nopeus = 1
        self.ennatyspisteet = 0
        self.soundraha = pygame.mixer.Sound("raha.wav")

        self.fontti = pygame.font.SysFont("Bahnschrift", 12)
        self.isofontti = pygame.font.SysFont("Stencil", 60)

        self.oikea, self.vasen, self.ylos, self.alas = False, False, False, False

        self.kello = pygame.time.Clock()
    
        self.silmukka()

    def uusi_peli(self):
        self.xr = 0
        self.yr = 0
        self.xp = self.leveys-self.roboleveys
        self.yp = self.korkeus-self.robokorkeus
        self.xk = randint(50, self.leveys-50)
        self.yk = randint(50, self.korkeus-50)
        self.pisteet = 0
        self.pahis_nopeus = 1
        

    def piirra_naytto(self):
        self.naytto.fill((10, 30, 255))
        self.naytto.blit(self.robo, (self.xr, self.yr))
        self.naytto.blit(self.pahis, (self.xp, self.yp))
        self.naytto.blit(self.kolikko, (self.xk, self.yk))
        piste_teksti = self.fontti.render(f"RAHAT: {self.pisteet}", True, (255, 255, 255))
        ohje_teksti = self.fontti.render("F2 = uusi peli     Esc = Poistu", True, (255, 255, 255))
        self.naytto.blit(ohje_teksti, (10, self.korkeus-20))
        self.naytto.blit(piste_teksti, (self.leveys-80, 0))
        if self.game_over():
            loppu_teksti = self.isofontti.render("GAME OVER!", True, (0, 0, 0))
            loppu_teksti2 = self.fontti.render(f"  SCORE: {self.pisteet}      HIGH SCORE: {self.ennatyspisteet}", True, (255, 255, 255))
            self.naytto.blit(loppu_teksti, (self.leveys/2-loppu_teksti.get_width()/2, 150))
            self.naytto.blit(loppu_teksti2, (self.leveys/2-loppu_teksti.get_width()/2, 200))
        
        pygame.display.flip()


    def silmukka(self):
        self.uusi_peli()
        while True:
            self.piirra_naytto()
            self.tapahtumat()

    def robon_liike(self):
        
        if self.oikea and self.xr < self.leveys-self.roboleveys:
            self.xr += 5
        if self.vasen and self.xr > 0:
            self.xr -= 5
        if self.ylos and self.yr > 0:
            self.yr -= 5
        if self.alas and self.yr < self.korkeus-self.robokorkeus:
            self.yr += 5

    def pahis_liike(self):
        
        if self.xp > self.xr:
            self.xp -= self.pahis_nopeus
        else:
            self.xp += self.pahis_nopeus
        if self.yp > self.yr:
            self.yp -= self.pahis_nopeus
        else:
            self.yp += self.pahis_nopeus

        if self.pisteet > 6:
            self.pahis_nopeus = 2
        if self.pisteet > 13:
            self.pahis_nopeus = 3
        if self.pisteet > 20:
            self.pahis_nopeus = 4
        

    def kolikon_liike(self):
        kolikko_keskipiste = (self.xk+self.kolikko.get_width()/2, self.yk+self.kolikko.get_height()/2)
        if kolikko_keskipiste[0] in range(self.xr, self.xr+self.roboleveys) and kolikko_keskipiste[1] in range(self.yr, self.yr+self.robokorkeus):
            self.pisteet += 1
            pygame.mixer.Sound.play(self.soundraha)
            if self.ennatyspisteet < self.pisteet:
                self.ennatyspisteet = self.pisteet
            self.xk = randint(40, self.leveys-40)
            self.yk = randint(40, self.korkeus-40)

    def game_over(self):
        robo_keskipiste = (self.xr+self.roboleveys/2, self.yr+self.robokorkeus/2)
        if robo_keskipiste[0] in range(self.xp, self.xp+self.pahis.get_width()) and robo_keskipiste[1] in range(self.yp, self.yp+self.pahis.get_height()):
            return True         

    def tapahtumat(self):
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    self.uusi_peli()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.vasen = True
                if event.key == pygame.K_RIGHT:
                    self.oikea = True
                if event.key == pygame.K_UP:
                    self.ylos = True
                if event.key == pygame.K_DOWN:
                    self.alas = True
     
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.vasen = False
                if event.key == pygame.K_RIGHT:
                    self.oikea = False
                if event.key == pygame.K_UP:
                    self.ylos = False
                if event.key == pygame.K_DOWN:
                    self.alas = False
            
            if event.type == pygame.QUIT:
                exit()

        if not self.game_over():
            self.robon_liike()
            self.pahis_liike()
            self.kolikon_liike()

        self.kello.tick(60)


if __name__ == "__main__":
    Peli()
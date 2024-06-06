# inisialisasi Game
import pygame
import random

# Resource Buat Sound dan font
pygame.font.init()
pygame.mixer.init()

# sound
sound_move = pygame.mixer.Sound("resource/sound/move.wav")
sound_rotasi = pygame.mixer.Sound("resource/sound/rotasi.wav")
sound_rowclear = pygame.mixer.Sound("resource/sound/rowclear.wav")
sound_gameover = pygame.mixer.Sound("resource/sound/gameover.wav")

# Warna Block
warna = [
    (255, 52, 153),
    (153, 51, 255),
    (51, 51, 255),
    (51, 255, 255),
    (51, 255, 153),
    (51, 255, 51),
    (153, 255, 51),
    (255, 255, 51),
    (255, 153, 51),
    (255, 51, 51),
]

# kelas untuk mengatur bentuk-bentuk blok yang akan ditampilkan
class BlokTetris:
    #mempresentasikan posisi blok diatas papan
    x = 0
    y = 0
    
    # matriks
    # 0     1       2       3
    # 4     5       6       7
    # 8     9       10      11
    # 12    13      14      15
    #Buat Bentuk Tetris
    blok_tetris = [
        [[1,5,9,13],[4,5,6,7]], #bentuk garis lurus
        [[4,5,9,10],[2,6,5,9]], #bentuk z
        [[6,7,9,10],[1,5,6,10]], #bentuk s
        [[1,2,5,9],[0,4,5,6],[1,5,9,8],[4,5,6,10]], #bentuk L
        [[1,2,6,10],[5,6,7,9],[2,6,10,11],[3,5,6,7]], #bentuk J
        [[1,4,5,6],[1,4,5,9],[4,5,6,9],[1,5,6,9]], #bentuk T
        [[1,2,5,6]], #bentuk o
        
    ]

    # method
    def __init__(self,x,y):
        self.x = x # menginisialisasi posisi awal `x` dan `y dari blok`
        self.y = y
        self.bentuk_blok = random.randint(0, len(self.blok_tetris) - 1)
        self.warna_blok = random.randint(1, len (warna) - 1)
        self.ubah_bentuk = 0
    
    def tampilan_blok(self): #mengembalikan array yang mempresentasikan posisi blok yang ditentukan oleh `bentuk_blok` dan `ubah_bentuk`
        return self.blok_tetris[self.bentuk_blok][self.ubah_bentuk]
    
    def putar(self): # mengubah nilai variabel `ubah_bentuk` sesuai dengan jumlah variasi bentuk `blok_tetris` yang dipilih serta digunakan untuk memutar bentuk blok tetris
        self.ubah_bentuk = (self.ubah_bentuk + 1) % len(self.blok_tetris[self.bentuk_blok])


# membuat dan mengatur objek-bjek yang mempresentasikan papan tetris
class Papan :
    # mempresentasikan posisi dan ukuran daru papan tetris
    x = 100
    y = 60
    zoom = 30
    
    # membuat objek `grid` yang berisi array 2D berukuran `tinggi` x `lebar`
    # setiap elemen dalam `grid` memiliki nilai awal 0
    # method
    def __init__(self, tinggi, lebar): 
        self.tinggi = tinggi
        self.lebar = lebar
        self.grid = []
        self.state = "start"    
        for i in range(tinggi):
            garis_grid = []
            for j in range(lebar):
                garis_grid.append(0)
            self.grid.append(garis_grid)
            
# membuat dan mengatur objek-objek yang merepresentasikan nilai/score dari permainan tetris
class Nilai(Papan) : # subclass dari class papan
    # method
    def __init__(self, tinggi, lebar):
        super().__init__(tinggi, lebar)
        self.nilai = 0
        self.jumlah_baris = 0
        self.state = "start"
        
    def BarisHilang(self):
        baris = 0
        for i in range(1, self.tinggi):
            zeros = 0
            for j in range(self.lebar):
                if self.grid[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                baris += 1
                self.jumlah_baris += 1
                pygame.mixer.Sound.play(sound_rowclear)
                for k in range(i, 1, -1):
                    for l in range(self.lebar):
                        self.grid[k][l] = self.grid[k - 1][l]

        if self.jumlah_baris <= 3 :
            if baris == 2 :
                self.nilai += (baris ** 2) -1
            if baris == 3 :
                self.nilai += (baris ** 4) -2
            if baris == 1 :
                self.nilai += (baris ** 2)
        else:
            self.nilai += 2 * self.jumlah_baris
            self.jumlah_baris = 0

# membuat dan mengatur objek-objek yang merepresentasikan menu pada perainan tetris 
class Menu(Nilai):# subclass dari class Nilai
    # method
    def __init__(self, tinggi, lebar) :
        super().__init__(tinggi, lebar)
        
    def MenuUtama(self):
        music = pygame.mixer.music.load("resource/sound/backsound.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        self.jenis_huruf = pygame.font.Font('resource/judul.ttf', 200)
        self.judul = self.jenis_huruf.render("Tetris" , True , (255,255,255))
        self.jenis_huruf = pygame.font.Font('resource/8bit.ttf', 100)
        self.menu_1 = pygame.Rect(self.lebar /2 - 110, self.tinggi - 85, 300, 100)
        self.menu_2 = pygame.Rect(self.lebar/2 - 110, self.tinggi + 85, 300, 100)
        return self.judul, self.menu_1 , self.menu_2
    
    def AmbilAksi(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_1.collidepoint(event.pos):
                    return True
                elif self.menu_2.collidepoint(event.pos):
                    pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                if self.menu_1.collidepoint(event.pos):
                    self.menu_1_color = (255, 0, 127)  # ubah warna tombol menu 1
                else:
                    self.menu_1_color = (127, 0, 255)  # kembalikan warna tombol menu 1
            elif event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.QUIT :
                pygame.quit()
        
        return None
                
class Tetris(Menu):
    level = 2
    blok = None
    
    def __init__(self, tinggi, lebar):
        super().__init__(tinggi, lebar)
        self.selanjutnya = None
        self.gameover = False
        self.BuatBlok()
        
    def BuatBlok(self):
        if not self.selanjutnya:
            self.selanjutnya = BlokTetris(5, 0)
        self.blok = self.selanjutnya
        self.selanjutnya = BlokTetris(5, 0)
    
    def CekLayar(self):
        batas_atas_layar = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.blok.tampilan_blok():
                    if i + self.blok.y > self.tinggi - 1 or \
                            j + self.blok.x > self.lebar - 1 or \
                            j + self.blok.x < 0 or \
                            self.grid[i + self.blok.y][j + self.blok.x] > 0:
                        batas_atas_layar = True
        return batas_atas_layar
    
    def BlokJatuh(self):
        self.blok.y += 1
        if self.CekLayar():
            self.blok.y -= 1
            self.BlokBerhenti()
    
    def BlokBerhenti(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.blok.tampilan_blok():
                    self.grid[i + self.blok.y][j + self.blok.x] = self.blok.warna_blok
        self.BarisHilang()
        self.BuatBlok()
        if self.CekLayar():
            self.state = "gameover"
    
    def GerakSamping(self, dx) :
        blok_sebelum_pindah = self.blok.x 
        self.blok.x += dx
        if self.CekLayar():
            self.blok.x = blok_sebelum_pindah
    
    def putar(self) :
        blok_sebelum_diubah = self.blok.ubah_bentuk
        self.blok.putar()
        pygame.mixer.Sound.play(sound_rotasi)
        if self.CekLayar():
            self.blok.ubah_bentuk = blok_sebelum_diubah  

# Setting Game
pygame.init()

hitam = (0,0,0)
putih = (255,255,255)
abu = (160,160,160)

Ukuran_layar = LEBAR, TINGGI = 700, 700
layar = pygame.display.set_mode(Ukuran_layar)

# Tambahkan gambar background pada menu utama
bg_menu = pygame.image.load('resource/bgmenu.jpg')
layar.blit(bg_menu, (0,0))

# tetris = Papan(20,10)
pygame.display.set_caption("Tetris")
berakhir = False
clock = pygame.time.Clock()
counter = 0
fps = 25
tetris = Tetris(20,10)

menu = Menu(480, 640)
judul, menu_1, menu_2 = menu.MenuUtama()
layar.blit(judul, [110,20])
start_game = False
gameover_sound_played = False
tekan_arah_bawah = False

while not start_game:
    # tampilkan tombol di layar
    pygame.draw.rect(layar, (255, 102, 178), menu_1, border_radius=20)
    layar.blit(menu.jenis_huruf.render("MULAI", True, (255, 255, 255)), (menu_1.x + 55, menu_1.y + 3))
    pygame.draw.rect(layar, (102, 102, 255), menu_2, border_radius=20)
    layar.blit(menu.jenis_huruf.render("KELUAR", True, (255, 255, 255)), (menu_2.x + 40, menu_2.y + 3))

    # periksa aksi yang diambil pengguna
    aksi = menu.AmbilAksi()
    if aksi:
        # tombol mulai diklik
        print("Mulai permainan!")
        start_game = True
    elif aksi is False:
        # tombol keluar diklik
        break

    # tampilkan layar
    pygame.display.update()

while not berakhir and start_game:
    if tetris.blok is None:
        tetris.BuatBlok()
    counter += 1
    if counter > 100000:
        counter = 0
    
    if counter % (fps // tetris.level // 2) == 0 or tekan_arah_bawah:
        if tetris.state == "start":
            tetris.BlokJatuh()  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berakhir = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetris.putar()
            if event.key == pygame.K_DOWN:
                pygame.mixer.Sound.play(sound_move)
                tekan_arah_bawah = True            
            if event.key == pygame.K_LEFT:
                pygame.mixer.Sound.play(sound_move)
                tetris.GerakSamping(-1)        
            if event.key == pygame.K_RIGHT:
                pygame.mixer.Sound.play(sound_move)
                tetris.GerakSamping(1)         
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                tekan_arah_bawah = False
    
        
    background = pygame.image.load('resource/background.jpg')
    layar.blit(background, (0, 0))
    logo = pygame.image.load('resource/logo.png')
    layar.blit(logo, (405, -50))
    jenis_huruf1 = pygame.font.Font('resource/8bit.ttf', 40)          
    blok_text = jenis_huruf1.render("NEXT", True, putih)
    blok_text_rect = blok_text.get_rect(center=(Ukuran_layar[0] - 150, Ukuran_layar[1] - 450))
    
    layar.blit(blok_text, blok_text_rect)

    # blok selanjutnya
    if tetris.selanjutnya:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.selanjutnya.tampilan_blok():
                    wrn = warna[tetris.selanjutnya.warna_blok]
                    x = LEBAR - 240 + 30 * (tetris.selanjutnya.x + j - 4) 
                    y = TINGGI - 410 + 30 * (tetris.selanjutnya.y + i) 
                    blok_area = pygame.Surface((30, 30))
                    blok_area.fill(wrn)
                    layar.blit(blok_area, (x, y))

    # menggambar grid
    for i in range(tetris.tinggi):
        for j in range(tetris.lebar):
            pygame.draw.rect(layar, abu, [tetris.x + tetris.zoom * j, tetris.y + tetris.zoom * i, tetris.zoom ,tetris.zoom], 1)
            if tetris.grid[i][j] > 0:
                pygame.draw.rect(layar, warna[tetris.grid[i][j]],
                                 [tetris.x + tetris.zoom * j + 1, tetris.y + tetris.zoom * i + 1, tetris.zoom - 2,tetris.zoom - 1])
        
    if tetris.blok is not None :
        kotak = pygame.image.load('resource/kotak.png')
        ukuran_kotak = pygame.transform.scale(kotak, (380, 380))
        layar.blit(ukuran_kotak, (358, 138))
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in tetris.blok.tampilan_blok():
                    pygame.draw.rect(layar, warna[tetris.blok.warna_blok],
                                     [tetris.x + tetris.zoom * (j + tetris.blok.x) + 1,
                                      tetris.y + tetris.zoom * (i + tetris.blok.y) + 1,
                                      tetris.zoom - 2, tetris.zoom - 2])

    jenis_huruf1 = pygame.font.Font('resource/8bit.ttf', 80)          
    score_text = jenis_huruf1.render("Score", True, putih)
    score_value = jenis_huruf1.render(str(tetris.nilai), True, putih)
    score_text_rect = score_text.get_rect(center=(Ukuran_layar[0] - 150, Ukuran_layar[1] - 150))
    score_value_rect = score_value.get_rect(center=(Ukuran_layar[0] - 150, Ukuran_layar[1] - 100))
    
    layar.blit(score_text, score_text_rect)
    layar.blit(score_value, score_value_rect)

    # gameover
    if tetris.state == "gameover":
        # Tambahkan gambar background pada menu 
        bg_menu = pygame.image.load('resource/bgmenu.jpg')
        layar.blit(bg_menu, (0,0))

        # tulisan game over
        game_over = pygame.image.load('resource/gameover.png')
        layar.blit(game_over, (120,50))

        # Tombol untuk pilihan 1
        tombol_pilihan_1 = pygame.Rect(LEBAR /2 - 150, TINGGI - 250, 300, 50)
        pygame.draw.rect(layar, (51, 51, 255), tombol_pilihan_1, border_radius=20)
        jenis_huruf2 = pygame.font.Font('resource/8bit.ttf', 45) 
        teks_pilihan_1 = jenis_huruf2.render("Permainan Baru",True,(255, 255, 255))
        layar.blit(teks_pilihan_1, [235, 455])
        if event.type == pygame.MOUSEBUTTONDOWN and tombol_pilihan_1.collidepoint(event.pos):
            pygame.mixer.Sound.play(sound_rowclear)
            tetris = Tetris(20,10) 

        # Tombol untuk pilihan 2
        tombol_pilihan_2 = pygame.Rect(LEBAR /2 + 220, TINGGI - 50, 120, 40)
        pygame.draw.rect(layar, (255, 51, 51), tombol_pilihan_2, border_radius=20)
        jenis_huruf2 = pygame.font.Font('resource/8bit.ttf', 45) 
        teks_pilihan_2 = jenis_huruf2.render("Keluar",True,(255, 255, 255))
        layar.blit(teks_pilihan_2, [585, 650])
        if event.type == pygame.MOUSEBUTTONDOWN and tombol_pilihan_2.collidepoint(event.pos):
            pygame.quit()

        if not gameover_sound_played:
            pygame.mixer.Sound.play(sound_gameover)
            gameover_sound_played = True
    else:
        gameover_sound_played = False

    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)
    
    
pygame.quit()
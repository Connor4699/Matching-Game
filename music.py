def music(music_name):
    pygame.mixer.music.load(music_name+".mp3")
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play(-1)
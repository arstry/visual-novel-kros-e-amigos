import pygame

def tocar_musica(caminho: str, volume: float = 0.2):
    # check para ver se o processo do mixer ainda está vivo par evitar de não tocar nada ao reabrir jogo no mesmo terminal
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    else:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Erro ao tocar '{caminho}': {e}")

def parar_musica(fade_ms: int = 500):
    if pygame.mixer.get_init():
        pygame.mixer.music.fadeout(fade_ms)
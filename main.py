"""
Módulo principal: Ponto de entrada do jogo.
Contém a classe principal que encapsula o loop do Pygame.
"""
import pygame
import sys
from core.engine import GameEngine
from core.asset_manager import AssetManager
from core.menu import MainMenu
from core.audio_manager import tocar_musica, parar_musica

class GameApp:
    """
    Classe responsável por gerenciar a janela, o loop de eventos e a renderização principal.
    """
    def __init__(self):
        """Inicializa os subsistemas do Pygame, variáveis de estado e carrega os assets."""
        pygame.init()
        
        self._largura = 1200
        self._altura = 900
        self._tela = pygame.display.set_mode((self._largura, self._altura))
        pygame.display.set_caption("Visual Novel - Kros & Amigos")

        # fonte
        self._fonte_principal = pygame.font.SysFont(None, 30)
        self._fonte_escolhas = pygame.font.SysFont(None, 28)
        self._fonte_status = pygame.font.SysFont(None, 24)
        self._fonte_gigante = pygame.font.SysFont(None, 64)

        self._menu = MainMenu(self._largura, self._altura)
        self._engine = GameEngine()
        self._assets = AssetManager()
        
        self._estado_jogo = "menu"
        self._rodando = True

        self._relogio = pygame.time.Clock()

        # timer
        self._esperando_timer = False
        self._tempo_inicio_timer = 0
        self._atraso_necessario = 0

        self._inicializar_dados()
        
        tocar_musica("assets/audio/menu.ogg", 0.2)

    def _inicializar_dados(self):
        """Carrega scripts, imagens e define a cena inicial."""
        self._engine.load_script_from_json("data/script.json")

        bgs = [
            ("bg_rua", "assets/street.png"), ("bg_corredor", "assets/school_hallway.png"), 
            ("bg_sala", "assets/school_classroom.png"), ("bg_parque", "assets/park.png"), 
            ("bg_lanchonete", "assets/diner.png"), ("bg_biblioteca", "assets/library.png"),
            ("bg_academia", "assets/gym.png"), ("bg_quarto", "assets/kros_room.png"), 
            ("bg_lab", "assets/computer_lab.png"), ("bg_cinema", "assets/cinema.png"), 
            ("bg_clube", "assets/literature_club.png"), ("bg_pizzaria", "assets/pizzeria.png"),
            ("bg_jumpscare", "assets/purple_jumpscare.png"), ("bg_praia", "assets/beach.png"), 
            ("bg_mar", "assets/sea.png"), ("bg_mar_monstro", "assets/sea_monster.png"), 
            ("bg_isekai", "assets/isekai_city.png")
        ]

        for key, path in bgs:
            self._assets.load_bg(key, path)

        fundo_preto = pygame.Surface((self._largura, self._altura))
        fundo_preto.fill((0, 0, 0))
        self._assets._images["bg_preto"] = fundo_preto

        self._assets.load_2x2_spritesheet("kros", "assets/kros.png")
        self._assets.load_4x2_spritesheet("lola", "assets/lola.png") 
        self._assets.load_2x2_spritesheet("bibi", "assets/bibi.png")
        self._assets.load_2x2_spritesheet("lily", "assets/lily.png")
        self._assets.load_2x2_spritesheet("white", "assets/mr_white.png")
        self._assets.load_2x2_spritesheet("lily_yandere", "assets/lily_yandere.png")
        self._assets.load_2x2_spritesheet("emilia", "assets/emilia.png")

        self._engine.start("casa1")

    def executar(self):
        """Inicia o loop principal do jogo."""
        while self._rodando:
            self._processar_eventos()
            self._atualizar_estado()
            self._renderizar()
            
            self._relogio.tick(60)
            
        pygame.quit()
        sys.exit()

    def _processar_eventos(self):
        """Lida com inputs do usuário"""
        cena_atual = self._engine.current_scene

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._rodando = False
                
            if self._estado_jogo == "menu":
                resultado = self._menu.update(evento)

                if resultado == "Iniciar":
                    parar_musica(500)
                    pygame.time.wait(500)
                    tocar_musica("assets/audio/game.ogg", 0.2)
                    self._estado_jogo = "jogo"
                elif resultado == "Sair":
                    self._rodando = False

            elif self._estado_jogo == "jogo":
                if evento.type == pygame.KEYDOWN and not self._esperando_timer:
                    if cena_atual and cena_atual.is_ending:
                        if evento.key == pygame.K_r:
                            self._engine.reset("casa1")
                            self._estado_jogo = "menu"
                            tocar_musica("assets/audio/menu.ogg", 0.2)
                    
                    elif cena_atual and not cena_atual.choices:
                        if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self._engine.advance_linear_scene()
                    
                    elif cena_atual and cena_atual.choices:
                        if pygame.K_1 <= evento.key <= pygame.K_9:
                            indice_escolha = evento.key - 49
                            # key fora do range é tratada como erro
                            try:
                                self._engine.make_choice(indice_escolha)
                            except IndexError:
                                print(f"Erro: Escolha {indice_escolha + 1} inválida para esta cena.")
                            except Exception as e:
                                print(f"Erro inesperado no input: {e}")

    def _atualizar_estado(self):
        """Atualiza a lógica de tempo e transições de cena."""
        cena_atual = self._engine.current_scene
        
        if cena_atual and cena_atual.scene_id in ["f_white_corta", "fnaf_jumpscare", "isekai_atropelamento_impacto"] and not self._esperando_timer:
            self._esperando_timer = True
            self._tempo_inicio_timer = pygame.time.get_ticks()
            
            if cena_atual.scene_id == "f_white_corta": 
                self._atraso_necessario = 1800
            elif cena_atual.scene_id == "fnaf_jumpscare": 
                self._atraso_necessario = 2000
            else: 
                self._atraso_necessario = 3000 

        if self._esperando_timer:
            if pygame.time.get_ticks() - self._tempo_inicio_timer >= self._atraso_necessario:
                self._esperando_timer = False
                self._engine.advance_linear_scene()

    def _renderizar(self):
        """Desenha todos os elementos visuais na tela."""
        self._tela.fill((0, 0, 0))
        cena_atual = self._engine.current_scene

        if cena_atual:
            if self._estado_jogo == "menu":
                self._menu.draw(self._tela)
            
            elif self._estado_jogo == "jogo":
                bg_img = self._assets.get_image(cena_atual.background_key)
                if bg_img:
                    self._tela.blit(pygame.transform.scale(bg_img, (self._largura, self._altura)), (0, 0))

                if cena_atual.is_ending:
                    texto_fim = self._fonte_gigante.render(cena_atual.text, True, (255, 255, 255))
                    rect_texto = texto_fim.get_rect(center=(self._largura // 2, self._altura // 2 - 30))
                    self._tela.blit(texto_fim, rect_texto)
                    
                    texto_replay = self._fonte_escolhas.render("[R] Pressione para Rejogar", True, (255, 255, 0))
                    rect_replay = texto_replay.get_rect(center=(self._largura // 2, self._altura // 2 + 50))
                    self._tela.blit(texto_replay, rect_replay)
                else:
                    if cena_atual.character_sprite and cena_atual.background_key != "bg_jumpscare":
                        sprite_img = self._assets.get_image(cena_atual.character_sprite)
                        if sprite_img:
                            sprite_rect = sprite_img.get_rect()
                            sprite_rect.bottomright = (self._largura - 100, self._altura - 150)
                            self._tela.blit(sprite_img, sprite_rect)

                    caixa_texto = pygame.Surface((self._largura, 200), pygame.SRCALPHA)
                    caixa_texto.fill((0, 0, 0, 220)) 
                    self._tela.blit(caixa_texto, (0, self._altura - 200))
                    
                    self._tela.blit(self._fonte_principal.render(cena_atual.text, True, (255, 255, 255)), (20, self._altura - 180))
                    
                    if not cena_atual.choices and cena_atual.next_scene_id and not self._esperando_timer:
                        self._tela.blit(self._fonte_escolhas.render("[ESPAÇO] para continuar...", True, (150, 150, 150)), (40, self._altura - 130))
                    elif cena_atual.choices and not self._esperando_timer:
                        y_offset = self._altura - 130
                        for i, escolha in enumerate(cena_atual.choices):
                            self._tela.blit(self._fonte_escolhas.render(f"[{i+1}] {escolha.text}", True, (255, 255, 0)), (40, y_offset))
                            y_offset += 30

                    y_status = 10
                    for personagem, valor in self._engine.affinities.items():
                        self._tela.blit(self._fonte_status.render(f"{personagem}: {valor}", True, (0, 255, 0)), (10, y_status))
                        y_status += 25

        pygame.display.flip()

if __name__ == "__main__":
    try:
        app = GameApp()
        app.executar()
    except KeyboardInterrupt:
        # pegar o ctrl c do terminal para evitar bug de fechamento indevido
        print("\nEncerrando graciosamente...")
    except Exception as e:
        # outros erros que houver 
        print(f"\nErro fatal na execução: {e}")
    finally:
        # O bloco finally GARANTE que o pygame.quit() rode, 
        # liberando a placa de som para a próxima vez que o jogo abrir
        pygame.quit()
        sys.exit()
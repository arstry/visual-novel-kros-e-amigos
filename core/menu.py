import pygame
from core.creditos import iniciar_creditos


class MainMenu:

    def __init__(self, largura, altura):

        self._largura = largura
        self._altura = altura

        self._opcoes = [
            "Iniciar",
            "Créditos",
            "Sair"
        ]

        self._fonte_titulo = pygame.font.SysFont(None, 72)
        self._fonte_opcoes = pygame.font.SysFont(None, 40)

        self._background = pygame.image.load("assets/menu/menu.png")
        self._background = pygame.transform.scale(
            self._background,
            (largura, altura)
        )

    @property
    def largura(self):
        return self._largura

    @property
    def altura(self):
        return self._altura

    @property
    def opcoes(self):
        return self._opcoes

    def update(self, evento):

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_1:
                return "Iniciar"

            elif evento.key == pygame.K_2:
                iniciar_creditos()

            elif evento.key == pygame.K_3:
                return "Sair"

        return None

    def draw(self, tela):

        altura_barra = 100

        background_redimensionado = pygame.transform.scale(
            self._background,
            (self._largura, self._altura - altura_barra)
        )

        tela.blit(background_redimensionado, (0, 0))

        # barra preta embaixo
        barra = pygame.Surface((self._largura, 100), pygame.SRCALPHA)
        barra.fill((0, 0, 0, 180))
        tela.blit(barra, (0, self._altura - 100))

        # opções lado a lado
        textos = []

        for i, opcao in enumerate(self._opcoes):

            texto = self._fonte_opcoes.render(
                f"[{i+1}] {opcao}",
                True,
                (255, 255, 255)
            )

            textos.append(texto)

        largura_total = (
            sum(t.get_width() for t in textos)
            + 80 * (len(textos) - 1)
        )

        x = (self._largura - largura_total) // 2
        y = self._altura - 65

        for texto in textos:
            tela.blit(texto, (x, y))
            x += texto.get_width() + 80
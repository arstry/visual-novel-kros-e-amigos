import pygame
import sys

def iniciar_creditos():

    LARGURA = 800
    ALTURA = 600

    tela = pygame.display.set_mode((LARGURA, ALTURA))

    fonte = pygame.font.SysFont("arial", 80, bold=True)

    creditos = creditos = [
    "",
    "KROS & AMIGOS",

    "LÍDER DO PROJETO",
    "Gabriel R. C. Mendonça",

    "DIRETOR DO JOGO",
    "Gabriel R. C. Mendonça",

    "DIRETOR CRIATIVO",
    "Gabriel R. C. Mendonça",

    "PRODUTOR EXECUTIVO",
    "Gabriel R. C. Mendonça",

    "DESENVOLVEDOR PRINCIPAL",
    "Rafael Campello Soares",

    "DIRETOR TÉCNICO",
    "Rafael Campello Soares",

    "PROGRAMADOR PRINCIPAL",
    "Rafael Campello Soares",

    "PROGRAMAÇÃO DE GAMEPLAY",
    "Rafael Campello Soares",

    "PROGRAMAÇÃO DE SISTEMAS",
    "Rafael Campello Soares",

    "PROGRAMAÇÃO DA ENGINE",
    "Rafael Campello Soares",

    "PROGRAMAÇÃO DE FERRAMENTAS",
    "Rafael Campello Soares",

    "IMPLEMENTAÇÃO",
    "Rafael Campello Soares",

    "OTIMIZAÇÃO",
    "Rafael Campello Soares",

    "GERENCIAMENTO DE BUILD",
    "Rafael Campello Soares",

    "CONTROLE DE VERSÃO",
    "Rafael Campello Soares",

    "DESIGN NARRATIVO",
    "Gabriel Carvalho Pires",

    "ESCRITA DO ROTEIRO",
    "Gabriel Carvalho Pires",

    "CRIAÇÃO DE MUNDO",
    "Gabriel Carvalho Pires",

    "ESCRITA DOS PERSONAGENS",
    "Gabriel Carvalho Pires",

    "DESIGN DE DIÁLOGOS",
    "Gabriel Carvalho Pires",

    "ESCRITA DAS CENAS",
    "Gabriel Carvalho Pires",

    "GAME DESIGN",
    "Gabriel R. C. Mendonça",

    "DIREÇÃO VISUAL",
    "Gabriel R. C. Mendonça",

    "DIREÇÃO DE ARTE",
    "Gabriel R. C. Mendonça",

    "CONCEPT ART",
    "Gabriel R. C. Mendonça",

    "DESIGN DE AMBIENTES",
    "Gabriel R. C. Mendonça",

    "COMPOSIÇÃO DE CENAS",
    "Gabriel R. C. Mendonça",

    "DIREÇÃO DE ANIMAÇÃO",
    "Gabriel R. C. Mendonça",

    "DIREÇÃO DE ÁUDIO",
    "Gabriel Carvalho Pires",

    "SELEÇÃO MUSICAL",
    "Gabriel Carvalho Pires",

    "DESIGN DE SOM",
    "Gabriel Carvalho Pires",

    "EFEITOS ATMOSFÉRICOS",
    "Gabriel Carvalho Pires",

    "SUPORTE DA COMUNIDADE",
    "Arthur Rafael da Silva Veado",

    "APOIADOR DO PROJETO",
    "Arthur Rafael da Silva Veado",

    "MASCOTE DA EQUIPE",
    "Arthur Rafael da Silva Veado",

    "MASCOTE OFICIAL",
    "Arthur Rafael da Silva Veado",

    "GARANTIA DE QUALIDADE",
    "Rafael Campello Soares",
    "Gabriel Carvalho Pires",
    "Gabriel R. C. Mendonça",

    "TESTES DE JOGO",
    "Amigos e Testadores",

    "AGRADECIMENTOS ESPECIAIS",

    "A todos que apoiam jogos indie",
    "À comunidade open source",
    "A todos os desenvolvedores de visual novel do mundo",
    "A todos que jogaram este jogo",

    "",
    "KROS & AMIGOS",
    "Obrigado por jogar."
    ]

    y = ALTURA

    clock = pygame.time.Clock()

    rodando = True

    while rodando:

        clock.tick(60)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        tela.fill((0, 0, 0))

        for i, linha in enumerate(creditos):

            texto = fonte.render(
                linha,
                True,
                (255, 220, 0)
            )

            escala = max(
                0.3,
                1 - ((ALTURA - y + i * 50) / 1000)
            )

            largura = texto.get_width() * escala
            altura = texto.get_height() * escala

            texto = pygame.transform.scale(
                texto,
                (int(largura), int(altura))
            )

            pos_y = y + i * 50

            x = (LARGURA - largura) // 2

            tela.blit(texto, (x, pos_y))

        y -= 1

        if y < -len(creditos) * 60:
            rodando = False

        pygame.display.flip()   
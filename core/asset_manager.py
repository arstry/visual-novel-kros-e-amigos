"""
Módulo core.asset_manager: Gerencia o carregamento, processamento e cache de recursos gráficos.
Implementa Herança e Polimorfismo na estratégia de fatiamento de spritesheets, tanto para nossos com grid 2x2 quanto para 4x2.
"""
import pygame
import os
import sys
from abc import ABC, abstractmethod

class SpriteLoader(ABC):
    """
    Classe Abstrata: Define a regra para carregadores de spritesheet.
    """
    @abstractmethod
    def get_positions(self, sheet: pygame.Surface) -> tuple[int, int, dict[str, tuple[int, int]]]:
        """
        Método Polimórfico: Deve retornar a largura/altura do quadrante 
        e o dicionário mapeando a 'expressão' para a (coluna, linha).
        """
        pass

class Grid2x2Loader(SpriteLoader):
    """Herança: Estratégia para carregar spritesheets em formato 2x2."""
    def get_positions(self, sheet: pygame.Surface) -> tuple[int, int, dict[str, tuple[int, int]]]:
        largura_quadrante = sheet.get_width() // 2
        altura_quadrante = sheet.get_height() // 2
        posicoes = {
            "feliz": (0, 0),
            "raiva": (1, 0),
            "triste": (0, 1),
            "corando": (1, 1)
        }
        return largura_quadrante, altura_quadrante, posicoes

class Grid4x2Loader(SpriteLoader):
    """Herança: Estratégia para carregar spritesheets em formato 4x2."""
    def get_positions(self, sheet: pygame.Surface) -> tuple[int, int, dict[str, tuple[int, int]]]:
        largura_quadrante = sheet.get_width() // 4
        altura_quadrante = sheet.get_height() // 2
        posicoes = {
            "feliz": (0, 0),
            "raiva": (2, 0),
            "triste": (1, 1),
            "corando": (3, 0)
        }
        return largura_quadrante, altura_quadrante, posicoes


class AssetManager:
    """Gerenciador central dos nossos assets."""
    def __init__(self):
        # Variável encapsulada
        self._images = {}

    def _resource_path(self, relative_path: str) -> str:
        """Resolve o caminho absoluto, mesmo com empacotamento via PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_bg(self, key: str, filepath: str):
        """Carrega um background inteiro; aqui a gente tem fallback cinza em caso de erro"""
        caminho_real = self._resource_path(filepath)
        try:
            self._images[key] = pygame.image.load(caminho_real).convert()
        except FileNotFoundError:
            # erro sendo tratado
            fallback = pygame.Surface((800, 600))
            fallback.fill((50, 50, 50))
            self._images[key] = fallback

    def _aplicar_chroma_key_tolerancia(self, surface: pygame.Surface) -> pygame.Surface:
        """Remove o fundo verde (chroma key) manipulando pixels."""
        surface = surface.convert_alpha()
        pixels = pygame.PixelArray(surface)
        largura, altura = surface.get_size()
        
        for x in range(largura):
            for y in range(altura):
                r, g, b, a = surface.unmap_rgb(pixels[x, y])
                if g > 150 and r < 100 and b < 100:
                    pixels[x, y] = (0, 0, 0, 0)
                    
        pixels.close()
        return surface

    def load_spritesheet(self, key_prefix: str, filepath: str, loader: SpriteLoader, margin: int = 5, altura_desejada: int = 400):
        """
        Delega a lógica de mapeamento para a classe loader fornecida (Polimorfismo).
        """
        caminho_real = self._resource_path(filepath)
        try:
            sheet = pygame.image.load(caminho_real).convert_alpha()
            # O AssetManager não precisa saber se é 2x2 ou 4x2, ele apenas chama o método polimórfico
            larg_quad, alt_quad, posicoes = loader.get_positions(sheet)
            self._processar_fatiamento(sheet, key_prefix, posicoes, larg_quad, alt_quad, margin, altura_desejada)
        except FileNotFoundError:
            print(f"Aviso: Spritesheet '{filepath}' não encontrada.")

    # Retrocompatibilidade: wrappers para os loaders antigos de 2x2 e 4x2
    def load_2x2_spritesheet(self, key_prefix: str, filepath: str, margin: int = 5, altura_desejada: int = 400):
        self.load_spritesheet(key_prefix, filepath, Grid2x2Loader(), margin, altura_desejada)

    def load_4x2_spritesheet(self, key_prefix: str, filepath: str, margin: int = 5, altura_desejada: int = 400):
        self.load_spritesheet(key_prefix, filepath, Grid4x2Loader(), margin, altura_desejada)

    def _processar_fatiamento(self, sheet, key_prefix, posicoes, larg_quadrante, alt_quadrante, margin, alt_desejada):
        """Recorta, limpa e redimensiona os quadrantes da spritesheet."""
        larg_total, alt_total = sheet.get_size()

        for expressao, (col, lin) in posicoes.items():
            x = (col * larg_quadrante) + margin
            y = (lin * alt_quadrante) + margin
            w = larg_quadrante - (margin * 2)
            h = alt_quadrante - (margin * 2)

            x = max(0, min(x, larg_total - 1))
            y = max(0, min(y, alt_total - 1))
            w = max(1, min(w, larg_total - x))
            h = max(1, min(h, alt_total - y))

            rect_corte = pygame.Rect(x, y, w, h)
            
            try:
                image_recortada = sheet.subsurface(rect_corte).copy()
            except ValueError:
                continue
            
            image_limpa = self._aplicar_chroma_key_tolerancia(image_recortada)

            proporcao = alt_desejada / h if h > 0 else 1
            nova_largura = int(w * proporcao)
            
            if nova_largura > 0 and alt_desejada > 0:
                image_final = pygame.transform.scale(image_limpa, (nova_largura, alt_desejada))
                self._images[f"{key_prefix}_{expressao}"] = image_final

    # Getter
    def get_image(self, key: str) -> pygame.Surface | None:
        """Recupera a imagem processada através da chave."""
        return self._images.get(key)
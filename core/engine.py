"""
Módulo core.engine: Contém o motor de regras, controle de roteamento e classes de cena.
Implementa Herança, Polimorfismo, Classes Abstratas e Encapsulamento.
"""
from abc import ABC, abstractmethod
import json
import random

class Choice:
    """Encapsula as escolhas disponíveis em uma cena."""
    def __init__(self, text: str, next_scene_id: str, stat_changes: dict = None):
        self._text = text
        self._next_scene_id = next_scene_id
        self._stat_changes = stat_changes if stat_changes else {}

    # Getters
    @property
    def text(self) -> str: return self._text
    @property
    def next_scene_id(self) -> str: return self._next_scene_id
    @property
    def stat_changes(self) -> dict: return self._stat_changes


class AbstractScene(ABC):
    """
    Classe Abstrata que contém a regra para qualquer tipo de cena.
    """
    def __init__(self, scene_id: str, text: str, background_key: str, character_sprite: str = None):
        # Variáveis encapsuladas
        self._scene_id = scene_id
        self._text = text
        self._background_key = background_key
        self._character_sprite = character_sprite

    # Getters e Setters (Requisito POO)
    @property
    def scene_id(self) -> str: 
        return self._scene_id

    @property
    def text(self) -> str: 
        return self._text

    @text.setter
    def text(self, value: str):
        if not isinstance(value, str):
            raise ValueError("O texto da cena deve ser uma string.")
        self._text = value

    @property
    def background_key(self) -> str: 
        return self._background_key

    @property
    def character_sprite(self) -> str: 
        return self._character_sprite

    @property
    @abstractmethod
    def is_ending(self) -> bool:
        """Método abstrato: As subclasses devem definir se são cenas finais."""
        pass

    @abstractmethod
    def get_next_scene(self, choice_index: int = None) -> str | None:
        """Método abstrato para Polimorfismo no roteamento."""
        pass


class DialogueScene(AbstractScene):
    """Herança: Representa uma cena normal de fluxo ou múltiplas escolhas."""
    def __init__(self, scene_id: str, text: str, background_key: str, character_sprite: str = None, next_scene_id: str = None):
        super().__init__(scene_id, text, background_key, character_sprite)
        self._next_scene_id = next_scene_id
        self._choices: list[Choice] = []

    @property
    def is_ending(self) -> bool:
        return False

    @property
    def next_scene_id(self) -> str: 
        return self._next_scene_id

    @property
    def choices(self) -> list[Choice]:
        return self._choices

    def add_choice(self, text: str, next_scene_id: str, stat_changes: dict = None):
        self._choices.append(Choice(text, next_scene_id, stat_changes))

    def get_next_scene(self, choice_index: int = None) -> str | None:
        """Polimorfismo: Retorna a ID da próxima cena com base na escolha do jogador."""
        if self._choices and choice_index is not None:
            if 0 <= choice_index < len(self._choices):
                return self._choices[choice_index].next_scene_id
        return self._next_scene_id


class EndingScene(AbstractScene):
    """Herança: Representa uma tela de fim de jogo ou rota."""
    def __init__(self, scene_id: str, text: str, background_key: str, character_sprite: str = None):
        super().__init__(scene_id, text, background_key, character_sprite)
        self._choices = [] 
        self.next_scene_id = None

    @property
    def choices(self) -> list:
        return self._choices

    @property
    def is_ending(self) -> bool:
        return True

    def get_next_scene(self, choice_index: int = None) -> str | None:
        """Polimorfismo: Uma cena de final de jogo não aponta para um próximo nó, agindo diferente para a choice final"""
        return None


class GameEngine:
    """Gerencia o estado global, roteamento de scripts e pontuações."""
    def __init__(self):
        self._scenes: dict[str, AbstractScene] = {}
        self._current_scene: AbstractScene | None = None
        self._affinities = {"Lola": 0, "Bibi": 0, "Lily": 0}
        self._fila_eventos: list[str] = []
        self._isekai_flag = False

    @property
    def current_scene(self) -> AbstractScene:
        return self._current_scene    

    @property
    def affinities(self) -> dict:
        return self._affinities

    def load_script_from_json(self, filepath: str):
        """Carrega a base de dados em JSON com tratamento de erro para keys fora do range."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                script_data = json.load(f)
                
            for scene_id, data in script_data.items():
                is_ending = data.get("is_ending", False)
                
                # Instanciamento polimórfico baseado na flag do JSON
                if is_ending:
                    scene = EndingScene(
                        scene_id=scene_id,
                        text=data.get("text", ""),
                        background_key=data.get("background_key"),
                        character_sprite=data.get("character_sprite")
                    )
                else:
                    scene = DialogueScene(
                        scene_id=scene_id,
                        text=data.get("text", ""),
                        background_key=data.get("background_key"),
                        character_sprite=data.get("character_sprite"),
                        next_scene_id=data.get("next_scene_id")
                    )
                    for choice_data in data.get("choices", []):
                        scene.add_choice(choice_data["text"], choice_data["next_scene_id"], choice_data.get("stat_changes"))
                        
                self._scenes[scene_id] = scene
                
        except FileNotFoundError:
            print(f"Erro Crítico: A base de dados '{filepath}' não foi encontrada.")
        except json.JSONDecodeError:
            print("Erro Crítico: Falha ao decodificar a sintaxe do arquivo JSON.")
        except Exception as e:
            print(f"Erro inesperado no carregamento da engine: {e}")

    def start(self, start_scene_id: str):
        self.reset(start_scene_id)

    def reset(self, start_scene_id: str):
        self._affinities = {chave: 0 for chave in self._affinities}
        self._fila_eventos.clear()
        self._isekai_flag = random.random() <= 0.20 # nossa constante de chance para o evento especial
        self._current_scene = self._scenes.get(start_scene_id)

    def _update_affinity(self, character: str, amount: int):
        if character in self._affinities:
            self._affinities[character] += amount

    def make_choice(self, choice_index: int):
        if self._current_scene and hasattr(self._current_scene, 'choices') and self._current_scene.choices:
            if 0 <= choice_index < len(self._current_scene.choices):
                choice = self._current_scene.choices[choice_index]
                for personagem, alteracao in choice.stat_changes.items():
                    self._update_affinity(personagem, alteracao)
                
                # Utiliza o polimorfismo para obter a próxima cena
                next_id = self._current_scene.get_next_scene(choice_index)
                if next_id:
                    self._rotear_ou_avancar(next_id)

    def advance_linear_scene(self):
        if self._current_scene and not self._current_scene.choices:
            next_id = self._current_scene.get_next_scene()
            if next_id:
                self._rotear_ou_avancar(next_id)

    def _rotear_ou_avancar(self, next_scene_id: str):
        # Lógica densa de roteamento
        if next_scene_id == "AVALIAR_FINAIS":
            self._avaliar_finais()
            
        elif next_scene_id == "VERIFICAR_EVENTOS_ESPECIAIS":
            lily_pts = self._affinities.get("Lily", 0)
            lola_pts = self._affinities.get("Lola", 0)
            bibi_pts = self._affinities.get("Bibi", 0)
            
            if bibi_pts >= 3 and lola_pts <= 0 and lily_pts <= 0:
                self._current_scene = self._scenes["bibi_praia_1"]
            elif lily_pts >= 3 and lola_pts <= 0 and bibi_pts <= 0:
                self._current_scene = self._scenes["ddlc_inicio"]
            elif lola_pts >= 3 and lily_pts <= 0 and bibi_pts <= 0:
                self._current_scene = self._scenes["fnaf_inicio"]
            else:
                self._fila_eventos = [nome for nome, pts in self._affinities.items() if pts >= 3]
                if not self._fila_eventos:
                    self._current_scene = self._scenes["d4_sozinho"]
                else:
                    self._rotear_proximo_evento()
                    
        elif next_scene_id == "PROXIMO_EVENTO_ESPECIAL":
            self._rotear_proximo_evento()
            
        elif next_scene_id == "ROTEAR_DIA2_LILY":
            self._current_scene = self._scenes["dia2_lily_raiva"] if self._affinities.get("Lily", 0) < 0 else self._scenes["dia2_lily_conversa"]
                
        elif next_scene_id == "ROTEAR_DIA2_LOLA":
            self._current_scene = self._scenes["dia2_lola_conversa"] if self._affinities.get("Lola", 0) > 0 else self._scenes["dia2_lola_bobao"]
                
        elif next_scene_id == "ROTEAR_DIA3_BIBI":
            if self._affinities.get("Bibi", 0) >= 2: self._current_scene = self._scenes["d3_bibi_inicio"]
            else: self._rotear_ou_avancar("ROTEAR_DIA3_LILY") 
                
        elif next_scene_id == "ROTEAR_DIA3_LILY":
            if self._affinities.get("Lily", 0) >= 2: self._current_scene = self._scenes["d3_lily_inicio"]
            else: self._rotear_ou_avancar("ROTEAR_DIA3_LOLA")
                
        elif next_scene_id == "ROTEAR_DIA3_LOLA":
            if self._affinities.get("Lola", 0) >= 2: self._current_scene = self._scenes["d3_lola_inicio"]
            else: self._rotear_ou_avancar("VERIFICAR_EVENTOS_ESPECIAIS")

        else:
            self._current_scene = self._scenes.get(next_scene_id)

    def _rotear_proximo_evento(self):
        if self._fila_eventos:
            menina_atual = self._fila_eventos.pop(0)
            self._current_scene = self._scenes.get(f"ev_especial_{menina_atual.lower()}")
        else:
            self._avaliar_finais()

    def _avaliar_finais(self):
        meninas_pontuadas = [nome for nome, pontos in self._affinities.items() if pontos >= 3]
        quantidade = len(meninas_pontuadas)

        if quantidade == 0:
            total_pontos = sum(self._affinities.values())
            if total_pontos <= 0 and self._isekai_flag:
                self._current_scene = self._scenes.get("isekai_atropelamento")
            else:
                self._current_scene = self._scenes.get("final_mr_white")
        elif quantidade == 1:
            self._current_scene = self._scenes.get(f"final_namoro_{meninas_pontuadas[0]}")
        else:
            cena_harem = self._scenes.get("final_harem_escolha")
            if isinstance(cena_harem, DialogueScene):
                cena_harem.choices.clear() 
                for menina in meninas_pontuadas:
                    cena_harem.add_choice(f"Escolher {menina}", f"final_namoro_{menina}")
                if quantidade == 3:
                    cena_harem.add_choice("Escolher TODAS (Harem Route)", "end_harem_king")
            self._current_scene = cena_harem
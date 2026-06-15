# Kros & Amigos — Visual Novel

Uma visual novel interativa desenvolvida em Python com Pygame. Acompanhe Kros e seus amigos em uma história com múltiplas escolhas, finais diferentes e eventos especiais.

## Como executar

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python main.py
```

## Requisitos

- Python 3.10+
- Pygame 2.x

## Estrutura do projeto

```
├── assets/          # Imagens, sprites e áudio
├── core/            # Código-fonte do motor do jogo
│   ├── engine.py    # Motor de cenas, escolhas e afinidades
│   ├── menu.py      # Tela inicial
│   ├── creditos.py  # Tela de créditos
│   ├── asset_manager.py
│   └── audio_manager.py
├── data/            # Script do jogo (JSON)
├── main.py          # Ponto de entrada
├── requirements.txt
└── README.md
```

## Funcionalidades

- Sistema de escolhas que afetam a narrativa
- Afinidade com personagens (Lola, Bibi, Lily)
- Múltiplos finais baseados nas escolhas
- Eventos especiais aleatórios
- Sprites animados e cenários variados
- Tela de créditos com rolagem

## Equipe

- Gabriel R. C. Mendonça
- Gabriel Carvalho Pires
- Rafael Capim Soares
- Arthur Rafael Silva Teixeira

## Controles

| Tecla      | Ação                          |
|------------|-------------------------------|
| Espaço     | Avançar diálogo               |
| 1-9        | Selecionar escolha            |
| ESC        | Voltar (créditos) / Sair      |
| R          | Recomeçar (tela de final)     |

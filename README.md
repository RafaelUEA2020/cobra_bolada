# 🐍 Snake Game - Python & Pygame

Um clássico **Jogo da Cobrinha** (*Snake*) desenvolvido em Python utilizando a biblioteca **Pygame**. O projeto foi construído do zero com foco total em arquitetura de software, aplicando os conceitos de **desacoplamento**, **modularização** e padrões de nomenclatura em inglês da indústria de desenvolvimento.

---

## 🎯 Sobre o Projeto

O objetivo do jogo é guiar a cobrinha pelo cenário para comer as maçãs geradas aleatoriamente. Cada maçã consumida aumenta o tamanho do corpo da cobra e a pontuação do jogador. O desafio termina se a cobrinha colidir com as bordas da janela ou com o próprio corpo.

### ✨ Funcionalidades Implementadas
* **Menu Inicial (Start Screen):** Tela de boas-vindas contendo o título do jogo e o manual completo de instruções dos controles.
* **Sistema de Pausa:** Permite interromper o fluxo da partida a qualquer momento sem perder o progresso atual.
* **Confirmação de Saída (Failsafe):** Tela de confirmação ao apertar `ESC` durante o gameplay para evitar desistências acidentais.
* **Pontuação em Tempo Real & High Score:** Um HUD completo que mostra os pontos atuais e salva de forma persistente o seu maior recorde em um arquivo de texto local (`high_score.txt`).
* **Arquitetura Baseada em Grid:** Movimentação e spawn de itens perfeitamente alinhados em uma grade lógica baseada nas dimensões configuradas.

---

## 📁 Estrutura de Arquivos

O projeto foi estruturado utilizando o conceito de pacotes do Python para isolar as responsabilidades de cada componente:

```text
meu_jogo/
│
├── assets/
│   ├── __init__.py        # Inicializador do pacote de recursos
│   └── config.py          # Constantes globais (Cores, FPS, Grid, Velocidade)
│
├── core/
│   ├── __init__.py        # Inicializador do pacote principal
│   ├── apple.py           # Lógica de posicionamento e desenho da maçã
│   ├── game.py            # Maestro do jogo (Loop principal, Estados e Eventos)
│   ├── hud.py             # Gerenciador de interfaces de texto (Menu, Pausa, Scores)
│   ├── screen.py          # Configurações de renderização da janela
│   └── snake.py           # Mecânicas de movimento, direção e corpo da cobra
│
└── high_score.txt         # Arquivo gerado automaticamente para salvar o recorde

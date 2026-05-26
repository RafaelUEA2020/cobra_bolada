# Arquitetura C4 - Snake Game

Este documento descreve a arquitetura do projeto usando o modelo C4 nas camadas Context, Container e Component.

Nao inclui a camada Code.

## 1. Context

```mermaid
C4Context
    title C4 Context - Snake Game

    Person(player1, "Jogador 1", "Usuario que joga usando as setas do teclado.")
    Person(player2, "Jogador 2", "Usuario opcional no modo multiplayer, usando W A S D.")

    System(snakeGame, "Snake Game", "Jogo local da cobrinha desenvolvido em Python com Pygame. Permite modo single player e multiplayer.")

    System_Ext(fileSystem, "Sistema de Arquivos Local", "Armazena o arquivo high_score.txt com o maior recorde.")
    System_Ext(pygameRuntime, "Pygame Runtime", "Biblioteca usada para janela, eventos de teclado, desenho e loop grafico.")

    Rel(player1, snakeGame, "Controla a cobra do jogador 1")
    Rel(player2, snakeGame, "Controla a cobra do jogador 2 no modo multiplayer")
    Rel(snakeGame, fileSystem, "Le e grava recorde")
    Rel(snakeGame, pygameRuntime, "Usa para renderizacao, eventos e janela")
```

### Responsabilidades

- O jogador interage com o jogo por teclado.
- O jogo controla estados como menu, partida, pausa, confirmacao de saida e fim de jogo.
- O Pygame fornece a infraestrutura grafica e de entrada.
- O sistema de arquivos local persiste o high score em `high_score.txt`.

## 2. Container

```mermaid
C4Container
    title C4 Container - Snake Game

    Person(player1, "Jogador 1", "Usa setas")
    Person(player2, "Jogador 2", "Usa W A S D no multiplayer")

    System_Boundary(gameSystem, "Snake Game") {
        Container(app, "Aplicacao Python", "Python", "Ponto de entrada do jogo. Inicializa e executa o loop principal.")
        Container(core, "Core do Jogo", "Python package", "Regras de jogo, entidades principais, HUD, tela e loop.")
        Container(client, "Cliente de Entrada", "Python package", "Mapeia teclas pressionadas para comandos de direcao e pausa.")
        Container(assets, "Configuracao e Assets Logicos", "Python package", "Constantes globais de tela, cores, fonte, velocidade e controles.")
        ContainerDb(highScore, "high_score.txt", "Arquivo texto", "Persistencia local do maior recorde.")
    }

    System_Ext(pygameRuntime, "Pygame Runtime", "Janela, eventos, renderizacao e temporizador.")

    Rel(player1, app, "Executa e joga")
    Rel(player2, app, "Participa no modo multiplayer")

    Rel(app, core, "Chama run_game()")
    Rel(core, client, "Consulta handle_keydown() para tratar teclado")
    Rel(core, assets, "Le configuracoes globais")
    Rel(client, assets, "Usa configuracoes conceituais de controle")
    Rel(core, highScore, "Le e grava recorde")
    Rel(core, pygameRuntime, "Usa eventos, timer, desenho e display")
```

### Containers do projeto

- `main.py`: ponto de entrada da aplicacao.
- `core`: pacote principal com loop, entidades, HUD e tela.
- `client`: pacote de entrada do usuario, hoje focado em teclado.
- `assets`: pacote de configuracao, cores, dimensoes e constantes.
- `high_score.txt`: arquivo gerado em runtime para salvar o recorde.

## 3. Component

```mermaid
C4Component
    title C4 Component - Core e Entrada do Snake Game

    Container_Boundary(appContainer, "Aplicacao Python") {
        Component(main, "main.py", "Python module", "Importa e executa run_game().")
    }

    Container_Boundary(coreContainer, "core") {
        Component(game, "core.game", "Modulo Python", "Coordena loop principal, estados, eventos, movimento, colisao, pontuacao e reinicio.")
        Component(screen, "core.screen.GameScreen", "Classe Python", "Cria janela, limpa fundo e atualiza display.")
        Component(snake, "core.snake.Snake", "Classe Python", "Representa cobra, direcao, movimento, crescimento, colisao e desenho.")
        Component(apple, "core.apple.Apple", "Classe Python", "Gera posicao valida para a maca e desenha o item.")
        Component(hud, "core.hud.HUD", "Classe Python", "Renderiza menu, placar, recorde, pausa, confirmacao e tela de fim.")
    }

    Container_Boundary(clientContainer, "client") {
        Component(controls, "client.controls", "Modulo Python", "Traduz KEYDOWN do Pygame em direcoes das cobras e toggle de pausa.")
    }

    Container_Boundary(assetsContainer, "assets") {
        Component(config, "assets.config", "Modulo Python", "Define dimensoes, FPS, cores, fonte, velocidade e mapas de controles.")
    }

    ContainerDb(highScore, "high_score.txt", "Arquivo texto", "Armazena o maior recorde.")
    System_Ext(pygameRuntime, "Pygame Runtime", "Eventos, display, fontes, superficies, retangulos e desenho.")

    Rel(main, game, "Executa run_game()")

    Rel(game, screen, "Cria e atualiza tela")
    Rel(game, snake, "Cria e controla snake1 e snake2")
    Rel(game, apple, "Cria e reposiciona maca")
    Rel(game, hud, "Atualiza placar e desenha telas de estado")
    Rel(game, controls, "Envia teclas para tratamento")
    Rel(game, config, "Le FPS, velocidade e constantes")

    Rel(controls, snake, "Solicita mudanca de direcao")
    Rel(controls, config, "Relaciona controles definidos para jogadores")

    Rel(screen, config, "Le largura, altura, titulo e cor de fundo")
    Rel(snake, config, "Le grid, limites e cores das cobras")
    Rel(apple, config, "Le grid, limites e cor da maca")
    Rel(hud, config, "Le fonte, cores e dimensoes")

    Rel(hud, highScore, "Le e grava recorde")

    Rel(screen, pygameRuntime, "Usa display")
    Rel(game, pygameRuntime, "Usa eventos e timer")
    Rel(snake, pygameRuntime, "Usa Rect e draw")
    Rel(apple, pygameRuntime, "Usa Rect e draw")
    Rel(hud, pygameRuntime, "Usa fontes e superficies")
```

### Componentes principais

- `core.game`: orquestrador da aplicacao. Decide modo single/multiplayer, processa eventos, move as cobras, verifica colisao e escolhe vencedor ou game over.
- `core.snake.Snake`: entidade da cobra. Controla posicao, direcao atual, direcao pendente, crescimento e colisoes.
- `core.apple.Apple`: entidade da maca. Sorteia posicao livre no grid e renderiza a maca.
- `core.hud.HUD`: interface textual. Desenha menu de modo, placares, recorde, pausa, confirmacao e fim de jogo.
- `core.screen.GameScreen`: encapsula a janela do Pygame.
- `client.controls`: traduz entrada de teclado em comandos do jogo.
- `assets.config`: centraliza constantes compartilhadas.

## Observacoes arquiteturais

- A arquitetura atual e modular e simples, adequada ao tamanho do projeto.
- O `core.game` concentra a maior parte da orquestracao e regras de fluxo.
- O projeto ja separa entrada (`client`), configuracao (`assets`) e dominio/renderizacao (`core`).
- `assets.config` possui mapas de controle declarados, mas o mapeamento efetivo esta em `client.controls`.
- O arquivo `high_score.txt` e uma dependencia de runtime, gerada quando um novo recorde e salvo.

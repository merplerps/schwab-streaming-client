from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from typing import Dict, List
import uuid

app = FastAPI()

# In-memory storage for games
games: Dict[str, Dict] = {}

# HTML template for the game
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Tic Tac Toe</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .game-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .board {
            display: grid;
            grid-template-columns: repeat(3, 100px);
            grid-gap: 5px;
            margin: 20px auto;
        }
        .cell {
            width: 100px;
            height: 100px;
            background-color: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .cell:hover {
            background-color: #d0d0d0;
        }
        .cell:disabled {
            cursor: default;
        }
        .status {
            font-size: 24px;
            margin: 20px 0;
            font-weight: bold;
        }
        .player-info {
            margin: 10px 0;
            font-size: 18px;
        }
        .btn {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
        .btn:hover {
            background-color: #45a049;
        }
        .btn:disabled {
            background-color: #cccccc;
            cursor: default;
        }
        .waiting {
            color: #666;
        }
        .win {
            background-color: #aaffaa;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>Tic Tac Toe</h1>
        <div class="player-info" id="playerInfo">Waiting for players...</div>
        <div class="status" id="status">Game not started</div>
        <div class="board" id="board">
            <div class="cell" data-index="0"></div>
            <div class="cell" data-index="1"></div>
            <div class="cell" data-index="2"></div>
            <div class="cell" data-index="3"></div>
            <div class="cell" data-index="4"></div>
            <div class="cell" data-index="5"></div>
            <div class="cell" data-index="6"></div>
            <div class="cell" data-index="7"></div>
            <div class="cell" data-index="8"></div>
        </div>
        <button class="btn" id="restartBtn" onclick="restartGame()">Restart Game</button>
        <button class="btn" id="newGameBtn" onclick="createNewGame()">New Game</button>
    </div>

    <script>
        let gameId = null;
        let playerSymbol = null;
        let ws = null;

        function connectWebSocket() {
            const url = window.location.href.replace('http', 'ws');
            ws = new WebSocket(url + 'ws/' + gameId);
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateGame(data);
            };
            
            ws.onopen = function() {
                console.log('Connected to WebSocket');
            };
            
            ws.onclose = function() {
                console.log('Disconnected from WebSocket');
            };
        }

        function createNewGame() {
            fetch('/create_game', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                gameId = data.game_id;
                connectWebSocket();
                document.getElementById('playerInfo').textContent = 'Game created! Waiting for opponent...';
                document.getElementById('status').textContent = 'Waiting for opponent';
            });
        }

        function restartGame() {
            if (gameId) {
                fetch(`/restart_game/${gameId}`, {
                    method: 'POST'
                });
            }
        }

        function updateGame(data) {
            // Update board
            const board = document.getElementById('board');
            const cells = board.querySelectorAll('.cell');
            
            data.board.forEach((cell, index) => {
                cells[index].textContent = cell;
                if (cell !== '') {
                    cells[index].disabled = true;
                }
            });
            
            // Update status
            const statusElement = document.getElementById('status');
            const playerInfoElement = document.getElementById('playerInfo');
            
            if (data.game_over) {
                if (data.winner) {
                    statusElement.textContent = `Player ${data.winner} wins!`;
                } else {
                    statusElement.textContent = "It's a draw!";
                }
                // Disable all cells
                cells.forEach(cell => {
                    cell.disabled = true;
                });
            } else {
                statusElement.textContent = `Current player: ${data.current_player}`;
                
                // Highlight current player's turn
                if (data.current_player === playerSymbol) {
                    statusElement.style.color = '#4CAF50';
                } else {
                    statusElement.style.color = '#333';
                }
            }
            
            // Update player info
            if (data.player1 && data.player2) {
                playerInfoElement.innerHTML = `
                    Player 1: ${data.player1} | Player 2: ${data.player2}
                    <br>
                    You are: ${playerSymbol || 'Waiting...'}
                `;
            } else if (data.player1) {
                playerInfoElement.innerHTML = `
                    Player 1: ${data.player1} | Waiting for opponent...
                    <br>
                    You are: ${playerSymbol || 'Waiting...'}
                `;
            }
            
            // Update cell click handlers
            cells.forEach((cell, index) => {
                if (data.current_player === playerSymbol && !data.game_over) {
                    // Use a proper function assignment to avoid CSP issues
                    cell.onclick = function() {
                        makeMove(index);
                    };
                } else {
                    cell.onclick = null;
                }
            });
        }

        function makeMove(index) {
            if (gameId && playerSymbol) {
                fetch(`/make_move/${gameId}/${index}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        player: playerSymbol
                    })
                });
            }
        }

        // Initialize the game
        window.onload = function() {
            createNewGame();
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get():
    return html

@app.post("/create_game")
async def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = {
        "board": ["", "", "", "", "", "", "", "", ""],
        "current_player": "X",
        "game_over": False,
        "winner": None,
        "player1": None,
        "player2": None,
        "ws_connections": {}
    }
    return {"game_id": game_id}

@app.post("/restart_game/{game_id}")
async def restart_game(game_id: str):
    if game_id in games:
        games[game_id] = {
            "board": ["", "", "", "", "", "", "", "", ""],
            "current_player": "X",
            "game_over": False,
            "winner": None,
            "player1": games[game_id].get("player1"),
            "player2": games[game_id].get("player2"),
            "ws_connections": {}
        }
        return {"status": "success"}
    return {"status": "error"}

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    if game_id not in games:
        await websocket.close(code=1002)  # Invalid game ID
        return

    await websocket.accept()
    
    # Assign player to the game
    game = games[game_id]
    player_symbol = None
    if not game["player1"]:
        game["player1"] = str(len(game["ws_connections"]) + 1)
        player_symbol = "X"
    elif not game["player2"]:
        game["player2"] = str(len(game["ws_connections"]) + 1)
        player_symbol = "O"
    else:
        # Game already has two players
        await websocket.close(code=1008)  # Policy violation
        return

    # Store the player symbol in the websocket connection for later use
    websocket.player_symbol = player_symbol
    game["ws_connections"][player_symbol] = websocket
    
    try:
        # Send initial game state to the player
        await websocket.send_text(json.dumps({
            "board": game["board"],
            "current_player": game["current_player"],
            "game_over": game["game_over"],
            "winner": game["winner"],
            "player1": game["player1"],
            "player2": game["player2"]
        }))
        
        while True:
            # Wait for messages from the player
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process move
            if "move" in message:
                index = message["move"]
                if 0 <= index <= 8:
                    # Validate move
                    if game["board"][index] == "":
                        game["board"][index] = player_symbol
                        
                        # Check for win or draw
                        winner = check_winner(game["board"])
                        if winner:
                            game["game_over"] = True
                            game["winner"] = winner
                        elif "" not in game["board"]:
                            game["game_over"] = True
                            game["winner"] = None  # Draw
                        else:
                            # Switch player
                            game["current_player"] = "O" if game["current_player"] == "X" else "X"
                        
                        # Broadcast updated game state to both players
                        broadcast_game_state(game_id)
                        
    except WebSocketDisconnect:
        # Remove player from game
        if player_symbol in game["ws_connections"]:
            del game["ws_connections"][player_symbol]
        if game["player1"] == player_symbol:
            game["player1"] = None
        elif game["player2"] == player_symbol:
            game["player2"] = None
        # Broadcast updated game state to remaining player
        if len(game["ws_connections"]) > 0:
            broadcast_game_state(game_id)

def check_winner(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != "":
            return board[i]
    
    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != "":
            return board[i]
    
    # Check diagonals
    if board[0] == board[4] == board[8] != "":
        return board[0]
    if board[2] == board[4] == board[6] != "":
        return board[2]
    
    return None

def broadcast_game_state(game_id):
    game = games[game_id]
    state = {
        "board": game["board"],
        "current_player": game["current_player"],
        "game_over": game["game_over"],
        "winner": game["winner"],
        "player1": game["player1"],
        "player2": game["player2"]
    }
    
    # Send to all connected players
    for websocket in game["ws_connections"].values():
        try:
            websocket.send_text(json.dumps(state))
        except:
            # Handle disconnected clients
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8111)
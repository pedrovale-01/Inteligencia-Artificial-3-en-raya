import tkinter as tk
from game import X, O, EMPTY, initial_state, player, result, terminal, winner, minimax


class App:
    # Colores
    BG      = "#f5f5f0"
    CELL    = "#ffffff"
    HOVER   = "#e8e8e0"
    X_COL   = "#c0392b"
    O_COL   = "#2980b9"
    BORDER  = "#cccccc"
    TEXT    = "#222222"
    DIM     = "#888888"
    WIN_BG  = "#ffeaa7"

    def __init__(self, root):
        self.root = root
        self.root.title("Tres en Raya")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        self.board     = initial_state()
        self.human     = X
        self.ai        = O
        self.game_over = False

        self._build()
        self._refresh()

    def _build(self):
        # Encabezado
        self.status_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Helvetica", 14), bg=self.BG, fg=self.TEXT,
                 pady=16).pack()

        # Tablero
        grid = tk.Frame(self.root, bg=self.BORDER)
        grid.pack(padx=24)

        self.btns = []
        for i in range(3):
            row = []
            for j in range(3):
                b = tk.Button(
                    grid, text="", font=("Helvetica", 32, "bold"),
                    width=3, height=1,
                    bg=self.CELL, fg=self.TEXT,
                    activebackground=self.HOVER,
                    relief="flat", bd=0, cursor="hand2",
                    command=lambda r=i, c=j: self._click(r, c)
                )
                b.grid(row=i, column=j, padx=1, pady=1)
                b.bind("<Enter>", lambda e, btn=b: self._hover(btn, True))
                b.bind("<Leave>", lambda e, btn=b: self._hover(btn, False))
                row.append(b)
            self.btns.append(row)

        # Botones inferiores
        bar = tk.Frame(self.root, bg=self.BG)
        bar.pack(pady=16)

        tk.Button(bar, text="Nueva partida", font=("Helvetica", 11),
                  bg=self.BG, fg=self.TEXT, relief="solid", bd=1,
                  padx=12, pady=4, cursor="hand2",
                  command=self._reset).pack(side="left", padx=6)

        tk.Button(bar, text="Cambiar lado", font=("Helvetica", 11),
                  bg=self.BG, fg=self.TEXT, relief="solid", bd=1,
                  padx=12, pady=4, cursor="hand2",
                  command=self._switch).pack(side="left", padx=6)

        self.legend = tk.Label(self.root, font=("Helvetica", 10),
                               bg=self.BG, fg=self.DIM, pady=4)
        self.legend.pack()
        self._update_legend()

    # ── Interacción ──────────────────────────────────────

    def _hover(self, btn, entering):
        if btn["text"] == "" and not self.game_over:
            btn.configure(bg=self.HOVER if entering else self.CELL)

    def _click(self, r, c):
        if self.game_over or self.board[r][c] != EMPTY:
            return
        if player(self.board) != self.human:
            return
        self.board = result(self.board, (r, c))
        self._refresh()
        if not self.game_over:
            self.status_var.set("La IA está pensando...")
            self.root.update_idletasks()
            self.root.after(200, self._ai_move)

    def _ai_move(self):
        action = minimax(self.board)
        if action:
            self.board = result(self.board, action)
        self._refresh()

    # Dibuj

    def _refresh(self):
        # Actualiza celdas y revisa si el juego terminó
        for i in range(3):
            for j in range(3):
                val = self.board[i][j]
                color = self.X_COL if val == X else self.O_COL if val == O else self.TEXT
                self.btns[i][j].configure(text=val or "", fg=color, bg=self.CELL)

        if terminal(self.board):
            self.game_over = True
            w = winner(self.board)
            if w == self.human:
                self.status_var.set("¡Ganaste!")
            elif w == self.ai:
                self.status_var.set("Ganó la IA")
            else:
                self.status_var.set("Empate")
            self._mark_winner()
            for row in self.btns:
                for b in row:
                    b.configure(state="disabled", cursor="arrow")
        else:
            turn = player(self.board)
            self.status_var.set("Tu turno" if turn == self.human else "Turno de la IA")

    def _mark_winner(self):
        # Pinta de amarillo la línea ganadora
        lines = (
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],
        )
        for line in lines:
            vals = [self.board[r][c] for r, c in line]
            if vals[0] and vals[0] == vals[1] == vals[2]:
                for r, c in line:
                    self.btns[r][c].configure(bg=self.WIN_BG)
                return

    #Control de partida

    def _reset(self):
        self.board = initial_state()
        self.game_over = False
        for row in self.btns:
            for b in row:
                b.configure(state="normal", cursor="hand2")
        self._refresh()
        if player(self.board) == self.ai:
            self.root.after(300, self._ai_move)

    def _switch(self):
        self.human, self.ai = self.ai, self.human
        self._update_legend()
        self._reset()

    def _update_legend(self):
        self.legend.configure(text=f"Tú eres {self.human}  ·  IA es {self.ai}")

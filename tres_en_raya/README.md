# Tres en Raya

Un juego de tres en raya donde juegas contra una IA que nunca falla.
Lo mejor que puedes lograr es un empate, así que el objetivo es no perder.

## Cómo ejecutarlo

Necesitas tener Python instalado (versión 3.8 o más nueva). Nada más.

```bash
python main.py
```

## Cómo se juega

- Tú eres X y la IA es O (puedes cambiarlo con el botón "Cambiar lado").
- Haz clic en la celda donde quieres poner tu ficha.
- La IA responde de inmediato con su mejor jugada.
- Cuando alguien gana, se resalta la línea ganadora en amarillo.

## Qué hay dentro

```
tres_en_raya/
├── main.py           → arranca el juego
├── game/
│   ├── logic.py      → las reglas: quién mueve, qué jugadas hay, quién ganó
│   └── minimax.py    → la IA: busca la mejor jugada posible
└── ui/
    └── app.py        → la ventana y todo lo visual
```

## Cómo funciona la IA

La IA usa un algoritmo**Minimax**: básicamente prueba todas las jugadas
posibles, imagina cómo respondería el rival, y elige la que le da mejor resultado.
Para que no tarde demasiado, usa una optimización llamada **poda alpha-beta**
que le permite descartar caminos que ya sabe que no van a ningún lado.

El resultado es que la IA juega perfecto. Si empiezas en el centro tienes más
chances de empatar, pero no de ganar.

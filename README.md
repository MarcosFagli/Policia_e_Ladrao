# Inteligencia Artificial

Trabalho em homenagem ao jogo "Atari Busy Police", apresentado a disciplina de Inteligencia Ariticial da Universidade Federal de São Carlos - UFSCar, graduando no curso de Engenharia de computação.

Disciplina cursada no oitavo semestre do curso e ministrada pelo Docente Doutor Murillo Naldi.

## Objetivo

O jogo acontece em um supermercado de dimensões 10 (no eixo horizontal) e 5 (no eixo vertical) onde o policial é o personagem principal e deve encontrar seu caminho até o ladrão, passando por obstáculos.

O jogo foi composto por 5 entidades:
a) Policial
b) Ladrão
c) Carrinho de compras
d) Escada
e) Escorregador

As posições dos elementos do cenário (escadas, carrinhos e escorregador) são definidas no programa.
As posições do policial e do ladrão são passadas por parâmetro.

A movimentação se dá da seguinte forma:
a) Move-se livremente pela horizontal.
b) A escada permite a subida ou descida.
c) O escorregador permite apenas descida.
d) O carrinho é um obstáculo que o personagem deve “pular”.
e) O personagem só pode “pular” o carrinho se as posições adjacentes estiverem vazias.

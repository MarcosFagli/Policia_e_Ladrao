# Inteligencia Artificial

Trabalho em homenagem ao jogo "Atari Busy Police", apresentado a disciplina de Inteligencia Ariticial da Universidade Federal de São Carlos - UFSCar, graduando no curso de Engenharia de computação.

Disciplina cursada no oitavo semestre do curso e ministrada pelo Docente Doutor Murillo Naldi.

Agradecimento a Yuce (https://github.com/yuce) pela biblioteca pyswip encontrada em https://github.com/yuce/pyswip, possibilitando a utilização da interface gráfica pyQt em python para demonstrativo dos resultados obtidos no prolog

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

## Execução do código
### Código em prolog

Para executar o código em prolog basta abrir o SWI-PROLOG e importar a base de conhecimento

```
?- ['policialadrao'].
```

Então a base de conhecimento será importada. Para executar o procedimento de busca, basta digitar:

```
?- solucao(estado(X,Y,Z,W), K).
```

Onde X é a coordenada x do policial, Y é a coordenada y do policial, Z é a coordenada x do ladrao, W é a coordenada y do ladrao e K é a lista de caminhos tomados pelo policial para chegar ao ladrao, neste, passar um parametro com a inicial maiuscula, pois será uma váriavel, por onde será retornado o resultado.

### Código em Python

Para executar o código em pyhton é necessário ter instalado o python 3 e o pyswip.
Para instalar o pyswip (linux MINT 19):

```
~$ sudo pip3 install pyswip
```

Uma vez instalado, basta executar no terminal:

```
$ python3 busyPolice.py
```
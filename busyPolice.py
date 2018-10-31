#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LICENSE FOR USING PYSWIP
Copyright (c) 2007-2018 Yüce Tekol

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from pyswip import Prolog

prolog = Prolog()

#escada possui andar abaixo, andar acima, e posicao x
prolog.assertz("escada(1,2,4)")
prolog.assertz("escada(2,3,1)")
prolog.assertz("escada(3,4,9)")
prolog.assertz("escada(4,5,6)")
prolog.assertz("escada(1,2,10)")
prolog.assertz("escada(2,5,3)")

#posicionamento dos carrinhonhos (x,y)
prolog.assertz("carrinho(4,3)")
prolog.assertz("carrinho(6,1)")
prolog.assertz("carrinho(4,5)")
prolog.assertz("carrinho(8,2)")

#funcoes auxiliares
prolog.assertz("ladrao(_,Yp,_,Yl) :- Yp =\= Yl")
prolog.assertz("ladrao(Xp,Yp,Xl,Yl) :- Yp == Yl, Xp =\= Xl")

#2 - Verificador se a direita está livre
prolog.assertz("livreDireita(Xp,Yp,Xl,Yl) :- Xp1 is Xp+1, Xp2 is Xp+2, carrinho(Xp1,Yp), not(carrinho(Xp2,Yp)), not(escada(Yp,_,Xp2)), not(escada(_,Yp,Xp2)), ladrao(Xp2,Yp,Xl,Yl)")

#3 - Verificador se a direita imediata está livre
prolog.assertz("livreIDireita(Xp,Yp) :- Xp1 is Xp+1, not(carrinho(Xp1,Yp))")

#4 - Verificador se a esquerda esta livre
prolog.assertz("livreEsquerda(Xp,Yp,Xl,Yl) :- Xp1 is Xp-1, Xp2 is Xp-2, carrinho(Xp1,Yp), not(carrinho(Xp2,Yp)), not(escada(Yp,_,Xp2)), not(escada(_,Yp,Xp2)), ladrao(Xp2,Yp,Xl,Yl)")

#5 - Verificador se a esquerda imediata está livre
prolog.assertz("livreIEsquerda(Xp,Yp) :- Xp1 is Xp-1, not(carrinho(Xp1,Yp))")

#6 - Função pertence que verifica a existência de um dado elemento 
prolog.assertz("pertence(Elem, [Elem|_])")
prolog.assertz("pertence(Elem, [_|Cauda]):- pertence(Elem, Cauda)")

#Acoes
#7 - Ação de andar para a direita
prolog.assertz("acao(aDireita, L, [[d,Xp2,Yp]|L], estado(Xp1,Yp,Xl,Yl), estado(Xp2,Yp,Xl,Yl)) :- Xp1 < 10, livreIDireita(Xp1,Yp), Xp2 is Xp1+1, not(pertence([d,Xp2,Yp],L))")

#8 - Ação de pular um carrinho quando esta a direita do policial
prolog.assertz("acao(pularCarrinhoD, L, [[pcd,Xps,Yp]|L], estado(Xpe,Yp,Xl,Yl), estado(Xps,Yp,Xl,Yl)) :- Xpe > 2, Xp1 is Xpe+1, Xps is Xpe+2, carrinho(Xp1,Yp), livreDireita(Xpe,Yp,Xl,Yl), not(pertence([pcd,Xps,Yp],L))")

#11 - Ação de subir na escada
prolog.assertz("acao(subir, L, [[s,Xp,Yp2]|L], estado(Xp,Yp1,Xl,Yl), estado(Xp,Yp2,Xl,Yl)) :- Yp1 < 5, escada(Yp1,Yp2,Xp), not(pertence([s,Xp,Yp1],L))")

#9 - Ação de andar para a esquerda
prolog.assertz("acao(aEsquerda, L, [[e,Xp2,Yp]|L], estado(Xp1,Yp,Xl,Yl), estado(Xp2,Yp,Xl,Yl)) :- Xp1 > 1, livreIEsquerda(Xp1,Yp), Xp2 is Xp1-1, not(pertence([e,Xp2,Yp],L))")

#10 - Ação de pular um carrinho quando esta a esquerda do policial
prolog.assertz("acao(pularCarrinhoE, L, [[pce,Xps,Yp]|L], estado(Xpe,Yp,Xl,Yl), estado(Xps,Yp,Xl,Yl)) :- Xpe < 9, Xp1 is Xpe-1, Xps is Xpe-2, carrinho(Xp1,Yp), livreEsquerda(Xpe,Yp,Xl,Yl), not(pertence([pce,Xps,Yp],L))")

#12 - Ação de descer da escada
prolog.assertz("acao(descer, L, [[d,Xp,Yp2]|L], estado(Xp,Yp1,Xl,Yl), estado(Xp,Yp2,Xl,Yl)) :- Yp1 >= 0, escada(Yp2,Yp1,Xp), not(pertence([d,Xp,Yp2],L))")

#1 - Consegue situação final
prolog.assertz("consegue(T, estado(X,Y,X,Y), T)")

#13 - Consegue intermediário
prolog.assertz("consegue(L, Estado2, L2) :- acao(_, L, L1, Estado2, Estado1), consegue(L1, Estado1, L2)")

#14 - Chamar consegue com estado inicial do policial(Xp,Yp) e do ladrao(Xl,Yl)
prolog.assertz("solucao(estado(X,Y,Z,W), L) :- acao(_, [[i,X,Y]], L1, estado(X,Y,Z,W), Estado1), consegue(L1, Estado1, L), !")



x = list(prolog.query("solucao(estado(1,1,9,1), X)"))

print(x)
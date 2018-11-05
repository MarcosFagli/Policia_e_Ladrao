%escada possui andar abaixo, andar acima, e posicao x
escada(1,2,4).
escada(2,3,1).
escada(3,4,9).
escada(4,5,6).
escada(1,2,10).
escada(2,5,3).


%posicionamento dos carrinhonhos (x,y)
carrinho(4,3).
carrinho(6,1).
carrinho(4,5).
carrinho(8,2).


%funcoes auxiliares
ladrao(_,Yp,_,Yl) :- Yp =\= Yl.
ladrao(Xp,Yp,Xl,Yl) :- Yp == Yl, Xp =\= Xl.

%2 - Verificador se a direita está livre
livreDireita(Xp,Yp,Xl,Yl) :- Xp1 is Xp+1, Xp2 is Xp+2, carrinho(Xp1,Yp), not(carrinho(Xp2,Yp)), not(escada(Yp,_,Xp2)), not(escada(_,Yp,Xp2)), ladrao(Xp2,Yp,Xl,Yl).

%3 - Verificador se a direita imediata está livre
livreIDireita(Xp,Yp) :- Xp1 is Xp+1, not(carrinho(Xp1,Yp)).

%4 - Verificador se a esquerda esta livre
livreEsquerda(Xp,Yp,Xl,Yl) :- Xp1 is Xp-1, Xp2 is Xp-2, carrinho(Xp1,Yp), not(carrinho(Xp2,Yp)), not(escada(Yp,_,Xp2)), not(escada(_,Yp,Xp2)), ladrao(Xp2,Yp,Xl,Yl).

%5 - Verificador se a esquerda imediata está livre
livreIEsquerda(Xp,Yp) :- Xp1 is Xp-1, not(carrinho(Xp1,Yp)).

%6 - Função pertence que verifica a existência de um dado elemento em uma lista
pertence(Elem, [Elem|_]).
pertence(Elem, [_|Cauda]):- pertence(Elem, Cauda).


%Ações
%7 - Ação de andar para a direita
acao(aDireita, L, [[d,Xp2,Yp]|L], estado(Xp1,Yp,Xl,Yl), estado(Xp2,Yp,Xl,Yl)) :- Xp1 < 10, livreIDireita(Xp1,Yp), Xp2 is Xp1+1, not(pertence([d,Xp2,Yp],L)).

%8 - Ação de pular um carrinho quando esta a direita do policial
acao(pularCarrinhoD, L, [[pcd,Xps,Yp]|L], estado(Xpe,Yp,Xl,Yl), estado(Xps,Yp,Xl,Yl)) :- Xpe > 2, Xp1 is Xpe+1, Xps is Xpe+2, carrinho(Xp1,Yp), livreDireita(Xpe,Yp,Xl,Yl), not(pertence([pcd,Xps,Yp],L)).

%11 - Ação de subir na escada
acao(subir, L, [[s,Xp,Yp2]|L], estado(Xp,Yp1,Xl,Yl), estado(Xp,Yp2,Xl,Yl)) :- Yp1 < 5, escada(Yp1,Yp2,Xp), not(pertence([s,Xp,Yp1],L)).

%9 - Ação de andar para a esquerda
acao(aEsquerda, L, [[e,Xp2,Yp]|L], estado(Xp1,Yp,Xl,Yl), estado(Xp2,Yp,Xl,Yl)) :- Xp1 > 1, livreIEsquerda(Xp1,Yp), Xp2 is Xp1-1, not(pertence([e,Xp2,Yp],L)).

%10 - Ação de pular um carrinho quando esta a esquerda do policial
acao(pularCarrinhoE, L, [[pce,Xps,Yp]|L], estado(Xpe,Yp,Xl,Yl), estado(Xps,Yp,Xl,Yl)) :- Xpe < 8, Xp1 is Xpe-1, Xps is Xpe-2, carrinho(Xp1,Yp), livreEsquerda(Xpe,Yp,Xl,Yl), not(pertence([pce,Xps,Yp],L)).

%12 - Ação de descer da escada
acao(descer, L, [[d,Xp,Yp2]|L], estado(Xp,Yp1,Xl,Yl), estado(Xp,Yp2,Xl,Yl)) :- Yp1 >= 0, escada(Yp2,Yp1,Xp), not(pertence([d,Xp,Yp2],L)).


%1 - Consegue situação final
consegue(T, estado(X,Y,X,Y), T).

%13 - Consegue intermediário
consegue(L, Estado2, L2) :- acao(_, L, L1, Estado2, Estado1), consegue(L1, Estado1, L2).

%14 - Chamar consegue com estado inicial do policial(Xp,Yp) e do ladrao(Xl,Yl)
solucao(estado(X,Y,Z,W), L) :- acao(_, [[i,X,Y]], L1, estado(X,Y,Z,W), Estado1), consegue(L1, Estado1, L).
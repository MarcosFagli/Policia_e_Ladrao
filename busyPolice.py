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
#Inserção da biblioteca Prolog
from pyswip import Prolog

#Bibliotecas para a interface gráfica Tkinter
from tkinter import *        
from PIL import ImageTk, Image

#Biblioteca time para efeitos na interface
import time



def temEscada(escada, coluna, linha):
	print("aki" + str(coluna) + ", " + str(linha))
	for i in range (0, len(escada)):
		if(escada[i][1] == linha and escada[i][2] == coluna):
			return True
		elif(escada[i][0] == linha and escada[i][2] == coluna):
			return True
	return False



#Auxiliares para posicionamento do ladrao e do policial
policiaX = 1
policiaY = 1
ladraoX = 1
ladraoY = 5

#Instanciação do prolog para utilizar a máquina de inferencia python
prolog = Prolog()

#posicionamento dos carrinhonhos (x,y)
carrinho = [[4,3],[6,1],[4,5],[8,2]]

for i in range(0,len(carrinho)-1):
	prolog.assertz("carrinho(" + str(carrinho[i][0]) + "," + str(carrinho[i][1]) + ")")


#escada possui andar abaixo, andar acima, e posicao x
escada = [[1,2,4],[2,3,1],[3,4,9],[4,5,6],[1,2,10],[2,5,3]]

for i in range(0,len(escada)-1):
	prolog.assertz("escada(" + str(escada[i][0]) + "," + str(escada[i][1]) + "," + str(escada[i][2]) + ")")

#funcoes auxiliares (PROLOG)
prolog.assertz("ladrao(_,Yp,_,Yl) :- Yp =\= Yl")
prolog.assertz("ladrao(Xp,Yp,Xl,Yl) :- Yp == Yl, Xp =\= Xl")

#2 - Verificador se a direita está livre (PROLOG)
prolog.assertz("livreDireita(Xp,Yp,Xl,Yl) :- Xp1 is Xp+1, Xp2 is Xp+2, carrinho(Xp1,Yp), not(carrinho(Xp2,Yp)), not(escada(Yp,_,Xp2)), not(escada(_,Yp,Xp2)), ladrao(Xp2,Yp,Xl,Yl)")

#3 - Verificador se a direita imediata está livre (PROLOG)
prolog.assertz("livreIDireita(Xp,Yp) :- Xp1 is Xp+1, not(carrinho(Xp1,Yp))")

#4 - Verificador se a esquerda esta livre (PROLOG)
prolog.assertz("livreEsquerda(Xp,Yp,Xl,Yl) :- Xp1 is Xp-1, Xp2 is Xp-2, carrinho(Xp1,Yp), not(carrinho(Xp2,Yp)), not(escada(Yp,_,Xp2)), not(escada(_,Yp,Xp2)), ladrao(Xp2,Yp,Xl,Yl)")

#5 - Verificador se a esquerda imediata está livre (PROLOG)
prolog.assertz("livreIEsquerda(Xp,Yp) :- Xp1 is Xp-1, not(carrinho(Xp1,Yp))")

#6 - Função pertence que verifica a existência de um dado elemento (PROLOG)
prolog.assertz("pertence(Elem, [Elem|_])")
prolog.assertz("pertence(Elem, [_|Cauda]):- pertence(Elem, Cauda)")

#Acoes
#7 - Ação de andar para a direita (PROLOG)
prolog.assertz("acao(aDireita, L, [[d,Xp2,Yp]|L], estado(Xp1,Yp,Xl,Yl), estado(Xp2,Yp,Xl,Yl)) :- Xp1 < 10, livreIDireita(Xp1,Yp), Xp2 is Xp1+1, not(pertence([d,Xp2,Yp],L))")

#8 - Ação de pular um carrinho quando esta a direita do policial (PROLOG)
prolog.assertz("acao(pularCarrinhoD, L, [[pcd,Xps,Yp]|L], estado(Xpe,Yp,Xl,Yl), estado(Xps,Yp,Xl,Yl)) :- Xpe > 2, Xp1 is Xpe+1, Xps is Xpe+2, carrinho(Xp1,Yp), livreDireita(Xpe,Yp,Xl,Yl), not(pertence([pcd,Xps,Yp],L))")

#11 - Ação de subir na escada (PROLOG)
prolog.assertz("acao(subir, L, [[s,Xp,Yp2]|L], estado(Xp,Yp1,Xl,Yl), estado(Xp,Yp2,Xl,Yl)) :- Yp1 < 5, escada(Yp1,Yp2,Xp), not(pertence([s,Xp,Yp1],L))")

#9 - Ação de andar para a esquerda (PROLOG)
prolog.assertz("acao(aEsquerda, L, [[e,Xp2,Yp]|L], estado(Xp1,Yp,Xl,Yl), estado(Xp2,Yp,Xl,Yl)) :- Xp1 > 1, livreIEsquerda(Xp1,Yp), Xp2 is Xp1-1, not(pertence([e,Xp2,Yp],L))")

#10 - Ação de pular um carrinho quando esta a esquerda do policial (PROLOG)
prolog.assertz("acao(pularCarrinhoE, L, [[pce,Xps,Yp]|L], estado(Xpe,Yp,Xl,Yl), estado(Xps,Yp,Xl,Yl)) :- Xpe < 8, Xp1 is Xpe-1, Xps is Xpe-2, carrinho(Xp1,Yp), livreEsquerda(Xpe,Yp,Xl,Yl), not(pertence([pce,Xps,Yp],L))")

#12 - Ação de descer da escada (PROLOG)
prolog.assertz("acao(descer, L, [[d,Xp,Yp2]|L], estado(Xp,Yp1,Xl,Yl), estado(Xp,Yp2,Xl,Yl)) :- Yp1 >= 0, escada(Yp2,Yp1,Xp), not(pertence([d,Xp,Yp2],L))")

#1 - Consegue situação final (PROLOG)
prolog.assertz("consegue(T, estado(X,Y,X,Y), T)")

#13 - Consegue intermediário (PROLOG)
prolog.assertz("consegue(L, Estado2, L2) :- acao(_, L, L1, Estado2, Estado1), consegue(L1, Estado1, L2)")

#14 - Chamar consegue com estado inicial do policial(Xp,Yp) e do ladrao(Xl,Yl) (PROLOG)
prolog.assertz("solucao(estado(X,Y,Z,W), L) :- acao(_, [[i,X,Y]], L1, estado(X,Y,Z,W), Estado1), consegue(L1, Estado1, L), !")



x = list(prolog.query("solucao(estado(" + str(policiaX) + "," + str(policiaY) + "," + str(ladraoX) + "," + str(ladraoY) + "), X)"))

resposta = str(x[0])

tam = len(resposta)

respostaTratada = resposta[6:tam-1]
respostaTratada = respostaTratada.split('A')
respostaTratada.pop(0)

listaTemp = []

for i in range (0,len(respostaTratada)-1):
	temp = respostaTratada[i].split(',')
	temp.pop(0)
	temp.pop(len(temp)-1)
	temp[1] = temp[1][0:2]
	listaTemp.append(temp)


listaTemp.reverse()

#Instanciação do objeto TK para interface gráfica
root = Tk()

#Configurando as camadas de exibição
imgbranco = ImageTk.PhotoImage(Image.open("branco.png"))
imgpoli = ImageTk.PhotoImage(Image.open("policial.png"))
imgladrao = ImageTk.PhotoImage(Image.open("ladrao.png"))
imgcar = ImageTk.PhotoImage(Image.open("carrinho.png"))
imgesc = ImageTk.PhotoImage(Image.open("escada.png"))
imgPoliEsc = ImageTk.PhotoImage(Image.open("policiaEscada.png"))

#Criando a primeira camada (mapa)
imglabel = []
for i in range (0,5):
	linha = []
	for j in range (0,10):
		if([j+1,5-i] in carrinho):
			linha.append(Label(root, image=imgcar).grid(row=i, column=j))
		else:
			linha.append(Label(root, image=imgbranco).grid(row=i, column=j))
	imglabel.append(linha)

#Impressão das escadas
for i in range(0, len(escada)):
	imglabel[5-escada[i][2]][escada[i][1]-1] = Label(root, image=imgesc).grid(row=5-escada[i][1], column=escada[i][2]-1)
	imglabel[5-escada[i][2]][escada[i][0]-1] = Label(root, image=imgesc).grid(row=5-escada[i][0], column=escada[i][2]-1)

#Criando a camada do policial
imglabel2 = Label(root, image=imgpoli).grid(row=5-policiaY, column=policiaX-1)
imglabel2 = Label(root, image=imgladrao).grid(row=5-ladraoY, column=ladraoX-1)

#Exibindo imagem inicial
root.update_idletasks()
root.update()

time.sleep(0.5)

imglabel[5-policiaY][policiaX-1] = Label(root, image=imgbranco).grid(row=5-policiaY, column=policiaX-1)
imglabel2 = Label(root, image=imgpoli).grid(row=5-int(listaTemp[0][1]), column=int(listaTemp[0][0])-1)

tinhaEscada = False
#Executando em loop a seguinte ordem: redesenha o lugar do mapa onde estava o policial; redesenha o policial; e aguarda um tempo até a próxima exibição (realizado desta maneira, uma vez que o processamento já foi realizado pela maquina de inferencia prolog)
for i in range (1, len(listaTemp)):

	colunaA = int(listaTemp[i-1][0])
	linhaA = int(listaTemp[i-1][1])
	coluna = int(listaTemp[i][0])
	linha = int(listaTemp[i][1])

	if(tinhaEscada):
		imglabel[5-linhaA][colunaA-1] = Label(root, image=imgesc).grid(row=5-linhaA, column=colunaA-1)
	else:
		imglabel[5-linhaA][colunaA-1] = Label(root, image=imgbranco).grid(row=5-linhaA, column=colunaA-1)
	
	if(temEscada(escada, coluna, linha)):
		imglabel2 = Label(root, image=imgPoliEsc).grid(row=5-linha, column=coluna-1)
		tinhaEscada = True
	else:
		imglabel2 = Label(root, image=imgpoli).grid(row=5-linha, column=coluna-1)
		tinhaEscada = False
	
	root.update_idletasks()
	root.update()

	time.sleep(1)

root.mainloop()




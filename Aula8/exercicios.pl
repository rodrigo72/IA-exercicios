soma_tres_valores(X,Y,Z, Soma) :-
	Soma is X + Y + Z.

soma_lista([], 0).
soma_lista([Head | Tail], Soma) :-
	soma_lista(Tail, SomaTail),
	Soma is Head + SomaTail.

max(X, Y, Maior) :-
	(X > Y ->
		Maior=X;
		Maior=Y
	).

max_lista([X], X).
max_lista([H | T], Result) :-
	max_lista(T, TMax),
	(H >= TMax -> Result = H ; Result = TMax).

calcula_media_aux([], C, Soma, Media) :-
	C > 0,
	Media is Soma / C.

calcula_media_aux([H | T], C, Soma, Media) :-
	C1 is C + 1,
	Soma1 is Soma + H,
	calcula_media_aux(T, C1, Soma1, Media).

calcula_media([], 0).
calcula_media(L, Media) :-
	calcula_media_aux(L, 0, 0, Media).

inserir_ordenado(Elemento, [], [Elemento]).

inserir_ordenado(Elemento, [Cabeca | Cauda], [Elemento, Cabeca | Cauda]) :-
	Elemento =< Cabeca.

inserir_ordenado(Elemento, [Cabeca | Cauda], [Cabeca | ListaOrdenada]) :-
	Elemento > Cabeca,
	inserir_ordenado(Elemento, Cauda, ListaOrdenada).

ordenar([], []).
ordenar([Head | Tail], Ordenada) :-
	ordenar(Tail, TailOrdenada),
	inserir_ordenado(Head, TailOrdenada, Ordenada).

pertence(X, [X | _]).
pertence(X, [Y | L]) :-
	X \= Y,
	pertence(X, L).
	
quantos([], 0).

quantos([X | L], N) :-
	pertence(X, L),
	!,
	quantos(L, N).

quantos([_ | L], N) :-
	quantos(L, TN),
	N is 1 + TN.

apagar(_, [], []).
apagar(X, [X | R], R) :- !.
apagar(X, [H | T], [H, Result]) :-
	apagar(X, T, Result).


aluno(1,joao,m).
aluno(2,antonio,m).
aluno(3,carlos,m).
aluno(4,luisa,f).
aluno(5,maria,f).
aluno(6,isabel,f).

curso(1,lei).
curso(2,miei).
curso(3,lcc).

%disciplina(cod,sigla,ano,curso)
disciplina(1,ed,2,1).
disciplina(2,ia,3,1).
disciplina(3,fp,1,2).

%inscrito(aluno,disciplina)
inscrito(1,1).
inscrito(1,2).
inscrito(5,3).
inscrito(5,5).
inscrito(2,5).

%nota(aluno,disciplina,nota)
nota(1,1,15).
nota(1,2,16).
nota(1,5,20).
nota(2,5,10).
nota(3,5,8).

%copia
copia(1,2).
copia(2,3).
copia(3,4).

aluno_sem_inscricao(Aluno) :-
	aluno(ID, Aluno, _),
	\+ inscrito(ID, _).

aluno_sem_inscricao_2(Aluno) :-
	aluno(ID, Aluno, _),
	\+ (inscrito(ID, ucID), disciplina(ucID, _, _, _)).

media_aluno(AlunoID, Media) :-
	aluno(AlunoID, _, _),
	findall(Nota, nota(AlunoID, _, Nota), Notas),
	length(Notas, NumUcs),
	sum_list(Notas, SomaNotas),
	(NumUcs > 0
		-> Media is SomaNotas / NumUcs
		; Media is 0
	).

media_global(Media) :-
	findall(Nota, nota(_, _, Nota), Notas),
	length(Notas, Len),
	sum_list(Notas, Sum),
	(Len > 0
		-> Media is Sum / Len
		; Media is 0
	).

alunos_acima_media(Alunos) :-
	media_global(MediaGlobal),
	findall(AlunoID, (media_aluno(AlunoID, Media), Media > MediaGlobal), Alunos).

copiou(AlunoID) :-
	copia(AlunoID, _).

copiou_por(Aluno1, Aluno2) :-
    (copia(Aluno1, Aluno), Aluno = Aluno2)
    ; copia(Aluno, Aluno2), copiou_por(Aluno, Aluno2).


alunos_copiaram(Nomes) :-
	findall(Nome, (aluno(ID, Nome, _), copiou(ID)), Nomes).

alunos_copiaram_por(AlunoID, Nomes) :-
	findall(Nome, (aluno(ID, Nome, _), copiou_por(ID, AlunoID)), Nomes).

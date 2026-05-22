:- dynamic presente/1.
:- dynamic bnp_elevado/0.
:- dynamic fevi_menor_50/0.
:- dynamic angina/0.

% ---------- Criterios de Framingham ----------

criterio_mayor(edema_pulmonar_agudo).
criterio_mayor(cardiomegalia).
criterio_mayor(reflujo_hepatoyugular).
criterio_mayor(distension_venas_cuello).
criterio_mayor(disnea_paroxistica_nocturna).
criterio_mayor(rales).
criterio_mayor(galope_tercer_ruido).

criterio_menor(edema_tobillos).
criterio_menor(disnea_esfuerzo).
criterio_menor(hepatomegalia).
criterio_menor(tos_nocturna).
criterio_menor(derrame_pleural).
criterio_menor(taquicardia).

count_mayores(N) :-
    findall(M, (criterio_mayor(M), presente(M)), L),
    length(L, N).

count_menores(N) :-
    findall(M, (criterio_menor(M), presente(M)), L),
    length(L, N).

% Regla diagnostica de Framingham (Tabla 6)
% IC = 2 criterios MAYORES  o  1 MAYOR + 2 MENORES
cumple_framingham :-
    count_mayores(N), N >= 2.
cumple_framingham :-
    count_mayores(NM), NM >= 1,
    count_menores(Nm), Nm >= 2.

% ---------- Arbol de decision (Figura 1) ----------

% Paso 1: aplicar Framingham + BNP
diagnostico(ic_descartada) :-
    \+ cumple_framingham,
    \+ bnp_elevado.

diagnostico(sospecha_diastolica) :-
    \+ cumple_framingham,
    bnp_elevado.

diagnostico(ic_sospechada) :-
    cumple_framingham.

% Paso 2: tipo segun FEVI (ecocardiografia)
tipo_ic(sistolica) :-
    diagnostico(ic_sospechada),
    fevi_menor_50.

tipo_ic(diastolica) :-
    diagnostico(ic_sospechada),
    \+ fevi_menor_50.

% Paso 3: coronariografia
requiere_coronariografia :- angina.

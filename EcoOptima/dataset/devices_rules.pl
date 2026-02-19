% Fatti: device(Nome, PotenzaKW, Priorita).
device(lavatrice, 2.0, bassa).
device(forno, 2.5, media).
device(lavastoviglie, 1.5, bassa).
device(frigo, 0.3, alta).
device(phon, 1.8, media).
device(auto_elettrica, 3.5, bassa).
device(asciugatrice, 2.0, bassa). % <-- INSERITO QUI, INSIEME AGLI ALTRI

% --- REGOLE ---

% Fatto: Definisce una dipendenza fisica/logica tra due dispositivi
depends_on(asciugatrice, lavatrice).

% Regola: high_load se potenza > 1.5kW
high_load(X) :- device(X, P, _), P > 1.5.

% Regola: incompatibili se entrambi high_load (rischio distacco contatore)
incompatible(X, Y) :- high_load(X), high_load(Y), X \= Y.

% Regola: preferibile usare di notte se priorità bassa
preferable_at_night(X) :- device(X, _, bassa).

% Regola: Y deve essere eseguito PRIMA di X se X dipende da Y.
must_run_before(Y, X) :- depends_on(X, Y).

% Regola: Un dispositivo è "critico" e non dovrebbe essere posticipato 
is_critical(X) :- device(X, _, alta).
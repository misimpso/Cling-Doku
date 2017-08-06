#const width=9.
#const height=9.
#const divs=3.
#const lower=3.
#const higher=5.

% Cell Values
values(1..width).

% Cell coordinates
coord((0..width-1, 0..height-1)).

% Find border coords and store them in border set
border(V-1) :- values(V), ((V - 1) \ divs) == 0.

% Tie coordinates to values
1 { cell(V, C) : values(V) } 1 :- coord(C).

% Create sets with coordinates connected with other coordinates by a direction

vertical((X1, Y1), (X2, Y2)) :- coord((X1, Y1)); coord((X2, Y2)); X1 == X2; not Y1 == Y2.

horizontal((X1, Y1), (X2, Y2)) :- coord((X1, Y1)); coord((X2, Y2)); Y1 == Y2; not X1 == X2.

% Constrict the rows and columns to not have the same value twice

:- coord(C1; C2); horizontal(C1, C2); cell(V1, C1); cell(V2, C2); V1 == V2.

:- coord(C1; C2); vertical(C1, C2); cell(V1, C1); cell(V2, C2); V1 == V2.

% Create set linking coordinates to their respective zone

zone((X1, Y1), B1, B2) :- border(B1), border(B2), coord((X1, Y1)); X1 >= B1, X1 < (B1 + 3), Y1 >= B2, Y1 < (B2 + 3).

% Create set joining coordinates based on their shared zone

zone_share(C1, C2) :- border(B1; B2); zone(C1, B1, B2); zone(C2, B1, B2).

% Constrict coordinates that share a zone to not have duplicate values

:- coord(C1; C2); zone_share(C1, C2); cell(V1, C1); cell(V2, C2); C1 != C2; V1 == V2.

lower { given(C) : zone(C, B1, B2) } higher :- border(B1), border(B2).

#show cell/2.
#show given/1.
#show zone/3.


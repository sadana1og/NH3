t(_)::c1. %developed
t(_)::c2. %agriculture
t(_)::c3. %herbaceous
t(_)::c4. %shrubland
t(_)::c5. %forest
t(_)::c6. %water

%developed
t(_)::c1 :- bareGroundNDVI.
t(_)::c1 :- scarceVegetationNDVI.
%t(_)::c1 :- iceAndSnowNDVI.
%t(_)::c1 :- waterNDVI.

%agriculture
t(_)::c2 :- bareGroundNDVI.
%t(_)::c2 :- scarceVegetationNDVI.
t(_)::c2 :- mediumVegetationNDVI.
%t(_)::c2 :- iceAndSnowNDVI.
%t(_)::c2 :- waterNDVI.

%herbaceous
t(_)::c3 :- mediumVegetationNDVI.
%t(_)::c3 :- iceAndSnowNDVI.
t(_)::c3 :- scarceVegetationNDVI.

%shrubland
t(_)::c4 :- bareGroundNDVI.
t(_)::c4 :- scarceVegetationNDVI.

%forest
t(_)::c5 :- mediumVegetationNDVI.
t(_)::c5 :- thickVegetationNDVI.

%water
t(_)::c6 :- waterNDVI.

t(_)::cloudsNDVI.
t(_)::bareGroundNDVI :- \+cloudsNDVI.
t(_)::iceAndSnowNDVI :- \+bareGroundNDVI.
t(_)::scarceVegetationNDVI :- \+iceAndSnowNDVI.
t(_)::mediumVegetationNDVI :- \+scarceVegetationNDVI.
t(_)::thickVegetationNDVI :- \+mediumVegetationNDVI.
t(_)::waterNDVI :- \+thickVegetationNDVI.

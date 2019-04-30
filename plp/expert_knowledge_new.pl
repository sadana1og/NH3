1.0::c1.
1.0::c2.
1.0::c3.
1.0::c4.
1.0::c5.
0.999999999999999::c6.
0.419875209527565::c1 :- bareGroundNDVI.
0.696223446813728::c1 :- scarceVegetationNDVI.
0.368065482364758::c2 :- bareGroundNDVI.
0.458943604890671::c2 :- mediumVegetationNDVI.
0.939697649676343::c3 :- mediumVegetationNDVI.
0.131616762976077::c3 :- scarceVegetationNDVI.
0.940179646068921::c4 :- bareGroundNDVI.
0.442268833161366::c4 :- scarceVegetationNDVI.
0.731361841768842::c5 :- mediumVegetationNDVI.
0.659888201533512::c5 :- thickVegetationNDVI.
0.931275629158072::c6 :- waterNDVI.
0.420289855071412::cloudsNDVI.
0.999999999997892::bareGroundNDVI :- \+cloudsNDVI.
1.0::iceAndSnowNDVI :- \+bareGroundNDVI.
0.382221577726337::scarceVegetationNDVI :- \+iceAndSnowNDVI.
1.0::mediumVegetationNDVI :- \+scarceVegetationNDVI.
1.0::thickVegetationNDVI :- \+mediumVegetationNDVI.
1.0::waterNDVI :- \+thickVegetationNDVI.

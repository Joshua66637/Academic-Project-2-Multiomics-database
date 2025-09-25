--Schema for database. GUID: 3047039
--A table that corresponds to the Subject entity
CREATE TABLE Subjects (
SubjectID VARCHAR(8) NOT NULL,
Race CHAR(1),
Sex CHAR(1),
Age DECIMAL(9, 2),
BMI DECIMAL(9, 2),
SSPG DECIMAL(9, 2),
IR_IS CHAR(2), 
PRIMARY KEY (SubjectID)
);

-- A table that corresponds to the BIOMOLECULE entity
CREATE TABLE Biomolecule (
SubjectID CHAR(8) NOT NULL,
VisitID CHAR(8) NOT NULL,
MoleculeID VARCHAR(30) NOT NULL,
OmicsType VARCHAR(30) NOT NULL,
ExpressionLevel DECIMAL(20, 10) NOT NULL,
PRIMARY KEY (SubjectID, VisitID, MoleculeID, OmicsType),
FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
);


-- A table that corresponds to the PeakAnnotation entity
CREATE TABLE PeakAnnotation (
PeakID VARCHAR(30) NOT NULL,
MetabolName VARCHAR(255) NOT NULL,
Kegg VARCHAR(255),
HMDB VARCHAR(255),
ChemClass VARCHAR(255),
Pathway VARCHAR(255),
PRIMARY KEY (PeakID, MetabolName),
FOREIGN KEY (PeakID) REFERENCES Biomolecule(MoleculeID)
);
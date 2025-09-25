"""This module aids in carrying out the repititive parts of the omics database building and querying process
It contains two classes: AbundanceProcessing which loads a file containing an omics table of molecular expression levels
and QueryDisplay which allows for the direct printing of results of sql queries 

"""
#Module called by main.py for omics data processing GUID:3047039
import sys
import sqlite3

class AbundanceProcessing:

    # constructor
    def __init__(self, molData, molType, omicdb):
        self._molData = molData
        self._molType = molType
        self._omicdb = omicdb
    
    # getter for molData
    @property
    def molData(self):
        return self._molData

    # getter for molType
    @property
    def molType(self):
        return self._molType

    # getter for omicdb
    @property
    def omicdb(self):
        return self._omicdb  

    def abundanceProcessor(self):
        """Loads a database using a file containing omics abundance data
        """
        try:
            with sqlite3.connect(self.omicdb) as connection:
                c = connection.cursor()
                omicsflag = True
                try:
                #Reading the abundance file
                    with open(self.molData) as MolData: 
                        #store names of all molecules from the header row
                        header = MolData.readline().strip().split("\t")
                        for line in MolData: 
                            #store the omics data values and customer and visit IDs from each line
                            MolInfo = line.replace("-","\t",1).strip().split("\t")
                            for i in range(2, len(MolInfo), 1):
                                #Customer and visit IDs are always the first two values
                                Abundance = [MolInfo[0], MolInfo[1], header[i-1], self.molType, MolInfo[i]]    
                                sqlAbundance = "INSERT INTO Biomolecule VALUES (?, ?, ?, ?, ?);"
                                try:
                                    c.execute(sqlAbundance, Abundance)
                                #In case of error, rollback the commands
                                except Exception as e:
                                    print("Could not load Biomolecule table with " + str(Abundance) + " since "+ str(e))
                                    connection.rollback()
                                    omicsflag = False
                                    break
                            if omicsflag:
                                connection.commit()   
                            else:
                                break             
                #Exit with error message if file is not found
                except FileNotFoundError: 
                    sys.exit(self.molData + " file not found. Please check and try again")
        #Exit with error message if database is not found
        except FileNotFoundError: 
                sys.exit(self.omicdb + " database not found. Please check and try again")

class QueryDisplay:
    
    # constructor
    def __init__(self, query, omicdb):
        self._query = query
        self._omicdb = omicdb
    
    # getter for query
    @property
    def query(self):
        return self._query
    
    # getter for omicdb
    @property
    def omicdb(self):
        return self._omicdb

    def __str__(self): #Using special method __str__ to display the results of any SELECT query
        try:
            with sqlite3.connect(self.omicdb) as connection:
                c = connection.cursor()
                Answer=""
                for row in c.execute(self.query):
                        #Used map function to convert each value of each row into a string then joined them using tabs and newlines
                        Answer= Answer + "\t".join(map(str,row)) + "\n" 
                return Answer[0:len(Answer)-1]
        #Exit with error message if database is not found
        except FileNotFoundError: 
                sys.exit(self.omicdb + " database not found. Please check and try again")
 
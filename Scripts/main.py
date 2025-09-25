#main program for GUID: 3047039
#Importing packages: sys for system exit, re for regex search, argparse to setup command line input 
import sys
import re
import argparse
import sqlite3

#Userdefined Module
import OmicsDataProcessor

#For query 9
import pandas as pd
import seaborn.objects as so

#Setting Up command line to accept the two input files using ArgParser
parser = argparse.ArgumentParser(description = "Multiomics Database Assessment", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--createdb", action='store_true', help = "This boolean flag creates the database")
parser.add_argument("--loaddb", action='store_true', help = "This boolean flag loads data into the database")
parser.add_argument("--querydb", type= int, default=0, help = "This optional integer argument chooses a predefined query from 1 to 9")
parser.add_argument("database", type= str, help = "The name of the database to be created")
parameters = parser.parse_args()

#Assigning File Locations from argparser to input variables
create = parameters.createdb
load = parameters.loaddb
query = parameters.querydb
omicdb = parameters.database

#Creating db
if(create):
    try:
        with sqlite3.connect(omicdb) as connection:
            c = connection.cursor()
            schemaflag = True
            try:
                script = ""
                with open("schema.sql") as file: #executing schema file
                    script = file.read()    
                connection.executescript(script)
            #In case of error, rollback the commands
            except Exception as e:
                print("Could not create schema for " + omicdb + " since "+ str(e))
                connection.rollback()
                schemaflag = False
            if schemaflag:
                connection.commit()
    #Exit with error message if database could not be opened
    except sqlite3.OperationalError:
        print("Failed to open database: " + omicdb)

#Loading db
if(load):
    subjects = "../data/Subject.csv"
    protData = "../data/HMP_proteome_abundance.tsv"
    transcriptData = "../data/HMP_transcriptome_abundance.tsv"
    metabolData = "../data/HMP_metabolome_abundance.tsv"
    metabolAnno = "../data/HMP_metabolome_annotation.csv"

    try:
        with sqlite3.connect(omicdb) as connection:
            c = connection.cursor()
            subjectsflag = True
            try:
            #Reading the Subjects file
                with open(subjects) as Subjects: 
                    header = Subjects.readline().strip().split(",")
                    for line in Subjects: 
                        SubjectInfo = line.upper().strip().split(",")
                        for i in range(0, len(SubjectInfo), 1): #Converting Unknown or NA values to None
                            if (SubjectInfo[i] == "UNKNOWN" or SubjectInfo[i] == "NA"):
                                SubjectInfo[i] = None

                        sqlSubject = "INSERT INTO Subjects VALUES (?, ?, ?, ?, ?, ?, ?);" #loading subject data into database
                        try:
                            c.execute(sqlSubject, SubjectInfo)
                        #In case of error, rollback the commands
                        except Exception as e:
                            print("Could not load Subjects table with " + str(SubjectInfo) + " since "+ str(e))
                            connection.rollback()
                            subjectsflag = False
                            break
                        if subjectsflag:
                            connection.commit()
                        else:
                            break                
            #Exit with error message if file is not found
            except FileNotFoundError: 
                sys.exit(subjects + " file not found. Please check and try again")
    #Exit with error message if database is not found
    except FileNotFoundError: 
            sys.exit(omicdb + " database not found. Please check and try again")

    #Loading the three omics abundance tables
    #Assigning an omicstype to each file
    files = [[protData, "Proteins"], [transcriptData, "Transcripts"], [metabolData, "Metabolites"]] 
    for omicsdata in files:
        Omicobj = OmicsDataProcessor.AbundanceProcessing(omicsdata[0], omicsdata[1], omicdb)#loading data using the user-defined module
        Omicobj.abundanceProcessor()

    try:
        with sqlite3.connect(omicdb) as connection:
            c = connection.cursor()
            annotflag = True
            try:
            #Reading the Annotations file
                with open(metabolAnno) as MetabolAnno:
                    moltype = "Metabolite" 
                    
                    header = MetabolAnno.readline().strip().split(",")
                    for line in MetabolAnno: 
                        MetabolInfo = re.subn("\([1-5]\)","",line)[0] #removing suffixes (1), (2) etc using regex
                        MetabolInfo = MetabolInfo.strip().split(",")
                        counter = 0

                        #counting the number of putative compounds linked to a single peak based on number of "|"
                        for i in range(0, len(MetabolInfo), 1):
                            MetabolInfo[i]= MetabolInfo[i].split("|")
                            if (MetabolInfo[i] == [""]):
                                MetabolInfo[i] = [None]
                            if(len(MetabolInfo[i])>counter):
                                counter = len(MetabolInfo[i])

                        #creating a new row for each compound linked to a single peak
                        for j in range(0, counter, 1):
                            annot = []
                            for i in range(0, len(MetabolInfo), 1):
                                try:
                                    if(MetabolInfo[i][0] == None):
                                        annot.append(MetabolInfo[i][0])
                                    else:
                                        annot.append(MetabolInfo[i][j].strip())
                                except IndexError:
                                        annot.append(MetabolInfo[i][0].strip())
                            
                            sqlAnnot = "INSERT INTO PeakAnnotation VALUES (?, ?, ?, ?, ?, ?);"
                            try:
                                c.execute(sqlAnnot, annot)
                            #In case of error, rollback the commands
                            except Exception as e:
                                print("Could not load PeakAnnotation table with " + str(annot) + " since "+ str(e))
                                connection.rollback()
                                annotflag = False
                                break
                        if annotflag:
                            connection.commit()
                        else:
                            break                
            #Exit with error message if file is not found
            except FileNotFoundError: 
                sys.exit(metabolAnno + " file not found. Please check and try again")
    #Exit with error message if database is not found
    except FileNotFoundError: 
        sys.exit(omicdb + " database not found. Please check and try again")

#querying db
if(query != 0):
    sql = ""
    match query:
        case 1:
            sql = """SELECT SubjectID, Age 
                    FROM Subjects 
                    WHERE Age>70;
                  """
        case 2:
            sql = """SELECT SubjectID 
                    FROM Subjects 
                    WHERE BMI BETWEEN 18.5 AND 24.9 AND Sex = "F" 
                    ORDER BY SubjectID DESC;
                  """
        case 3:
            sql = """SELECT DISTINCT VisitID
                    FROM Biomolecule
                    WHERE SubjectID = "ZNQOVZV"; 
                  """ 
        case 4:
            sql = """SELECT DISTINCT Subjects.SubjectID 
                    FROM Subjects, Biomolecule 
                    WHERE OmicsType = "Metabolites" AND IR_IS = "IR"; 
                  """  
        case 5:
            sql = """SELECT DISTINCT Kegg
                    FROM PeakAnnotation
                    WHERE PeakID IN ("nHILIC_121.0505_3.5", "nHILIC_130.0872_6.3", "nHILIC_133.0506_2.3", "nHILIC_133.0506_4.4"); 
                  """ 
        case 6:
            sql = """SELECT MIN(Age) AS Minimum_Age,
                    MAX(Age) AS Maximum_Age,
                    AVG(Age) AS Average_Age
                    FROM Subjects;
                  """  
        case 7:
            sql = """SELECT Pathway,
                    Count(Pathway)
                    FROM PeakAnnotation
                    GROUP BY Pathway
                    HAVING COUNT(Pathway) >= 10
                    ORDER BY COUNT(Pathway) DESC;
                  """
        case 8:
            sql = """SELECT MAX(ExpressionLevel) AS Max_Expression
                    FROM Biomolecule
                    WHERE SubjectID = "ZOZOW1T" AND MoleculeID = "A1BG" AND OmicsType = "Transcripts";
                  """
        case 9:
            sql = """SELECT Age, BMI 
                    FROM Subjects
                    WHERE (Age IS NOT NULL) AND (BMI IS NOT NULL);
                  """
            try:
                with sqlite3.connect(omicdb) as connection: 
                    AgeBMI= pd.read_sql(sql, connection)
                    p = so.Plot(AgeBMI, x= "Age", y= "BMI")
                    p = p.add(so.Dot(color= "green", pointsize = 3))
                    p.save("age_bmi_scatterplot.png")
            #Exit with error message if database is not found
            except FileNotFoundError: 
                sys.exit(omicdb + " database not found. Please check and try again")       
        #Exit with error message if the query is not a number from 1-9
        case _:
            print("Query must be a number from 1 to 9 only")
    print(OmicsDataProcessor.QueryDisplay(sql, omicdb))
                

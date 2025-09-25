# Project Title: Multiomics Database
## Course: Programming and Databased (MSc Bioinformatics) 

## Overview
This project describes the creation of a **bioinformatics database** containing multiomics data measurements and their related annotations. The data includes Transcriptomic, Proteomic and Metabolic data   
These measurements were collected from a **cohort of 106 subjects** as part of a study on aging markers.

## Data Description
For the data, we use a subset of a complex multi-omics dataset from the paper:  
*Personal aging markers and ageotypes revealed by deep longitudinal profiling*  
([Nature Medicine, 2020](https://www.nature.com/articles/s41591-019-0719-5)).    

### Data Files
- **Subject.csv**  
  Contains subject-level information.  
  - `SubjectID`: uniquely identifies each anonymised subject.  
  - Other information includes race, sex, age, body mass index (BMI) and steady-state plasma glucose (SSPG) level.

- **HMP_transcriptome_abundance.tsv, HMP_proteome_abundance.tsv, HMP_metabolome_abundance.tsv**  
  - Tab-separated files containing transcriptomics, proteomics, and metabolomics measurements.  

- **HMP_metabolome_annotation.csv**  
  - Links metabolite peaks to biological information such as Metabolite name, KEGG ID, HMDB ID and Chemical class  

## Implementation
- Built using **Python 3.10.9**  
- Database implemented with the **sqlite3** package  

## Usage
Run the program with:

```bash
python <program>.py [--createdb] [--loaddb] [--querydb=n] <SQLite database file>
Options
--createdb: Creates the database structure.
--loaddb: Parses the data files and inserts the relevant data into the database.
--querydb=n: Runs one of nine predefined queries (where n is a number from 1 to 9) on the database.
```
## Reference
Ahadi, S., Zhou, W., Schüssler-Fiorenza Rose, S. M., Sailani, M. R., Contrepois, K., Avina, M., Ashland, M., Brunet, A., & Snyder, M. (2020).
Personal aging markers and ageotypes revealed by deep longitudinal profiling.
Nature Medicine, 26(1), 83–90.
https://doi.org/10.1038/s41591-019-0719-5

# TWFYPreprocessor.py

## TheyWorkForYouPreprocessor

## Description
A Python data preprocessor that prepares raw XML data files for sentiment analysis. The raw XML data files containing division data are merged into an intermediate file. These files are then iterated through, in a process that assigns vote labels to speech tags by matching MP 'person-id' attributes. The labelled speech tags are then extracted and written to a separate JSON file format. 

The raw XML data files presented a number of challenges:

- The metadata needed to be understood in order to correctly extract the desired data
- Not all speech content corresponded to a division vote
    - Without a division vote, it wasn't possible to label the relevant speech content. The decision was therefore made to filter out this speech content during preprocessing.
- Circa 2015, the attributes used to identify MPs ("id") and speakers ("speakerid") was standardised into the uniform "person_id"
    - It was therefore necessary to rename any instances of MP "id" or speaker "speakerid" prior to 2015 so that all speech content attributes are consistent. 

## Usage
Run the application. The constants at the top of the page point to the relevant dataset filepaths - these can be changed if necessary. 

## Roadmap
Ideally, in the interest of saving time, this application would skip steps if no further changes need to be made to specific files, i.e. skipping the intermediate merged file stage if these files already exist. 

Due to the numerous stages of preprocessing and the time it takes to run the program, terminal loading bars might provide a clearer visual cue of the preprocessing progress. 
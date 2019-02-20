# MTG Sort:
I wanted a quick way to find information on all the cards I have, so I wrote a program to do that. Use the provided csv to see how information should be organized.

## Usage
Currently the program looks for a *csv* on the desktop with the cards in it. This directory can be changed by modifying the `read_csv()` function. Additionally, currently the `get_user_input()` is commented out but you can uncomment this to choose which attributes you want written to the output *csv*. 

Lastly, the program stores the entire set of data in memory to reduce API calls. This shouldn't be that large of a file and it only stores one set in memory at a time. 

**The program does use the  Scryfall API. Rate limiting is already in place but please don't abuse their API.**

### Future Features:
 1. Clean up code (this was initially quickly written for my use only)
 2. Integration with Google Sheets
 3. Fuzzy finding columns with pandas
 4. Convert to CLI tool with more options on output

# CryptoTwitPredict

To collect data:
1. install dependencies:
$ pip install -r requirements.txt
2. Make a copy of TwitterAuth.json into TwitterAuth_override.json, and add your Twitter API key in the new file.
This file is listed in .gitignore to prevent accidentally uploading the API key (I've had to revoke my key twice already becuase of this mistake)
$ cp TwitterAuth.json TwitterAuth_override.json
$ vi TwitterAuth_override.json
3. Run CollectInitialData.py - this outputs data into InitialData_[date].txt
$ ./CollectInitialData.py

To convert between data types:
1. determine the input data type and output data type:
CollectInitialData.py outputs in json_linedel
csv is a good format for use in Excel
json is ok for any other data analysis in python
$ ./ConvertData.py [input type] [input file] [output type] [output file]

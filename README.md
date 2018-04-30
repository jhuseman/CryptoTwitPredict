# CryptoTwitPredict



# To collect data:

1. install dependencies:

$ pip install -r requirements.txt

2. Make a copy of TwitterAuth.json into TwitterAuth_override.json, and add your Twitter API key in the new file.

This file is listed in .gitignore to prevent accidentally uploading the API key (I've had to revoke my key twice already because of this mistake)

$ cp TwitterAuth.json TwitterAuth_override.json

$ vi TwitterAuth_override.json

3. Run CollectInitialData.py - this outputs data into InitialData_[date].txt

$ ./CollectInitialData.py



# To convert between data types:

1. determine the input data type and output data type:

CollectInitialData.py outputs in jsonl (json lines)

csv is a good format for use in Excel

json is ok for any other data analysis in python

add _sent to the end of the type to perform sentiment analysis during the conversion

array_sent_json is an optimized format for plotting in python, as it loads directly into an array, well suited for matplotlib.

$ ./ConvertData.py [input type] [input file] [output type] [output file]



# To combine two or more sets of data, simply run the command:

$ ./ConcatData.py [in_type in_file] [in_type2 in_file2] [in_type_n in_file_n] ... [out_type out_file]

This script does not properly handle the array_sent_json format, so when concatenating those (much more efficient to combine this way), instead use the command:

$ ./ConcatArrayData.py [in_file1] [in_file2] [in_file_n] ... [out_type]



# To plot data, run the command:

$ ./PlotData.py [in_type] [in_file]

This converts the data to array_sent_json format and stores it to a file, if it is not already in that format, then plots the data.  Change the keys used in lines 30-32 to plot the data differently.

This is much faster if run with a file already in array_sent_json format.









# Miscellaneous commands used to generate graphs

$ ./PlotArrayData.py data/CombinedData_to_Mon_Mar_19_16_15_22_2018at.sent.arr.json unixtime BTC

$ ./AnalyzeAndPlotArrayData.py data/CombinedNoText.arr.json data/Analyzed0.1.arr.json 0.1 unixtime polarity unixtime BTC

$ ./AnalyzeAndPlotArrayData.py data/CombinedNoText.arr.json data/Analyzed0.2.arr.json 0.2 days polarity days subjectivity days num_records days BTC days ETH


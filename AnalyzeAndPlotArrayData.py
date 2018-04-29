#! /usr/bin/env python

"""
Do an analysis on the given data in arr_json file, and save it to a file.
"""

import sys
from PlotArrayData import plot_data
from PlotArrayData import get_kwargs_raw as plot_args
from AnalyzeArrayData import analyze_file
from AnalyzeArrayData import save_to_file
from AnalyzeArrayData import get_kwargs_raw as analysis_args

def get_kwargs():
	"""returns the arguments that should be given to the plot_data function"""
	analysis_kwargs = analysis_args(sys.argv[:4])
	plot_kwargs = plot_args([sys.argv[0], "None"] + sys.argv[4:])
	return [analysis_kwargs, plot_kwargs]

if __name__ == "__main__":
	PARAMS = get_kwargs()
	ANALYSIS_KWARGS = PARAMS[0]
	PLOT_KWARGS = PARAMS[1]
	DATA = analyze_file(ANALYSIS_KWARGS[0], ANALYSIS_KWARGS[2])
	save_to_file(DATA, ANALYSIS_KWARGS[1])
	plot_data(DATA, PLOT_KWARGS[1])

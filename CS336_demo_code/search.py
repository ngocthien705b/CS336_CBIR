# $ python search.py {--index index.csv} --query queries/108100.png {--result-path dataset} )(--num_results 5)

# import the necessary packages
from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

# ap.add_argument("-i", "--index", required = True,
# 	help = "Path to where the computed index will be stored")

ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")

# ap.add_argument("-r", "--result-path", required = True,
# 	help = "Path to the result path")

ap.add_argument("-n", "--num_results", required = False,
	help = "Number of results")

args = vars(ap.parse_args())

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
query = cv2.imread(args["query"])
features = cd.describe(query)

# perform the search
searcher = Searcher("index.csv")
num_results = 5
if (args["num_results"]):
	num_results = int(args["num_results"])
results = searcher.search(features, num_results)

# display the query
height = 600
width = int((height / query.shape[0]) * query.shape[1])
query = cv2.resize(query, (width, height))

cv2.imshow(args["query"], query)
cv2.waitKey(0)

query_file_name = os.path.basename(args["query"])
query_file_name = os.path.splitext(query_file_name)[0]
query_file_name = query_file_name.rstrip('0123456789')

true_positive = 0
false_positive = 0
# loop over the results
for (score, resultID) in results:
	# load the result image and display it
	# result = cv2.imread(args["result_path"] + "/" + resultID)
	result = cv2.imread(resultID)
	height = 600
	width = int((height / result.shape[0]) * result.shape[1])
	result = cv2.resize(result, (width, height))
	cv2.imshow(resultID, result)
	cv2.waitKey(0)

	result_file_name = os.path.basename(resultID)
	result_file_name = os.path.splitext(result_file_name)[0]
	result_file_name = result_file_name.rstrip('0123456789')
	
	if (query_file_name == result_file_name):
		true_positive += 1
	else:
		false_positive += 1

n = 20
print("True positive: ", true_positive)
print("False positive: ", false_positive)
print("False negative: ", n - true_positive)
print("Precision: ", true_positive / (true_positive + false_positive))
print("Recall: ", true_positive / n)
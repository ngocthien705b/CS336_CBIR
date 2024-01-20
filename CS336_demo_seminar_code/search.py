# $ python search.py (--index index.csv) --query queries/108100.png (--result-path dataset)

# import the necessary packages
from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--index", required = True,
# 	help = "Path to where the computed index will be stored")

ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")

# ap.add_argument("-r", "--result-path", required = True,
# 	help = "Path to the result path")

args = vars(ap.parse_args())

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
query = cv2.imread(args["query"])
features = cd.describe(query)

# perform the search
searcher = Searcher("index.csv")
results = searcher.search(features, 5)

# display the query
height = 600
width = int((height / query.shape[0]) * query.shape[1])
query = cv2.resize(query, (width, height))
cv2.imshow("Query", query)
cv2.waitKey(0)

i = 0
# loop over the results
for (score, resultID) in results:
	if i==5: break
	i += 1

	# load the result image and display it
	# result = cv2.imread(args["result_path"] + "/" + resultID)
	result = cv2.imread(resultID)
	height = 600
	width = int((height / result.shape[0]) * result.shape[1])
	result = cv2.resize(result, (width, height))
	cv2.imshow("Result", result)
	cv2.waitKey(0)

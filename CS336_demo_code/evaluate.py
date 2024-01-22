from colordescriptor import ColorDescriptor
from searcher import Searcher
import cv2
import os
import csv

# initialize the image descriptor
cd = ColorDescriptor((8, 10, 8))
searcher = Searcher("index.csv")

def test(query_img):
    # load the query image and describe it
    query = cv2.imread(query_img)
    features = cd.describe(query)

    # perform the search
    num_results = 20
    results = searcher.search(features, num_results)

    # query
    query_file_name = os.path.basename(query_img)
    query_file_name = os.path.splitext(query_file_name)[0]
    query_file_name = query_file_name.rstrip('0123456789')

    ans = [query_file_name, query_img]

    true_positive = 0
    false_positive = 0
    # loop over the results
    for (score, resultID) in results:
        # load the result image and display it
        result_file_name = os.path.basename(resultID)
        result_file_name = os.path.splitext(result_file_name)[0]
        result_file_name = result_file_name.rstrip('0123456789')
    
        if (query_file_name == result_file_name):
            true_positive += 1
        else:
            false_positive += 1

    ans.append(true_positive)
    ans.append(false_positive)

    false_negative = num_results - true_positive
    ans.append(false_negative)

    precision = true_positive / (true_positive + false_positive)
    ans.append(precision)

    recall = true_positive / num_results
    ans.append(recall)

    f1 = 2 * (precision * recall) / (precision + recall)
    ans.append(f1)

    return ans

path = "query_imgs"
files = os.listdir(path)

data = [["Topic", "Input image", "True positive", "False positive", "False negative", "Precision", "Recall", "F1 score"]]

for file in files:
    data.append(test(path + "/" + file))

with open("evaluate_result.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)
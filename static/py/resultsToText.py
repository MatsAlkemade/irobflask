import pandas as pd

file1 = "ResultsTemplateMatching"
file2 = "barcode_db"
# 
# read_file = pd.read_csv(f"{file2}.txt")
# read_file.to_csv(rf'{file2}.csv', index=None)

def writeToFile(results):
    file1 = open("ResultsTemplateMatching.txt", "w")
    file1.write("accuracy_score, template_name, datetime\n")
    for result in results:
        file1.write(str(result)+"\n")
    file1.close()

def textToCSV():
    read_file = pd.read_csv(f"{file2}.txt")
    read_file.to_csv(rf'{file2}.csv', index=None)


# writeToFile("Value: 0.99%")
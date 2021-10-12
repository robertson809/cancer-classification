import time
import os
import pandas as pd
import csv

root_path = "../data/"
targets = ['Breast Invasive Carcinoma/', 'Lung Adenocarcinoma/',
           'Pancreatic Adenocarcinoma/', 'Kidney Renal Clear Cell Carcinoma/',
           'Lung Squamous Cell Carcinoma/', 'Uveal Melanoma/']
tiny_tar = {'Breast Invasive Carcinoma/': 0, 'Lung Adenocarcinoma/':
            1, 'Pancreatic Adenocarcinoma/': 2,
            'Kidney Renal Clear Cell Carcinoma/': 3,
            'Lung Squamous Cell Carcinoma/': 4,
            'Uveal Melanoma/': 5}
inverted_dict = dict([[v,k] for k, v in tiny_tar.items()])


def read():
    """
    Reads in the patient data. The paring of patient to target is
    implicit within the list. The features in list position i have the
    target classification i.
    """
    target_list = []
    df_list = []
    for cancer in targets:
        for dirname in os.listdir(root_path + cancer):
            if dirname == 'MANIFEST.txt':
                continue
            for filename in os.listdir(root_path + cancer + dirname):
                if filename == 'annotations.txt':
                    continue
                print('reading file', filename, 'for cancer', cancer, end='')
                data = pd.read_csv(root_path + cancer + dirname + '/' + filename, sep='\t',
                                   usecols=['reads_per_million_miRNA_mapped', 'miRNA_ID'])
                data = pd.DataFrame.transpose(data)
                column_list = list(data.iloc[0])
                data.columns = column_list
                data.drop('miRNA_ID', axis=0, inplace=True)
                df_list.append(data)
                print(int(tiny_tar[cancer]))
                target_list.append(int(tiny_tar[cancer]))
    big_data = pd.concat(df_list)
    big_data.to_csv("../data/cleaned/features.csv")
    with open('../data/cleaned/targets.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(target_list)


if __name__ == "__main__":
    start = time.time()
    print('Running main')
    file = open('log.txt', 'w')
    file.write('Start time {0:.2f}\nEnd time {1:.2f}\nTotal time {2:.2f}'.format(
        start / 60, time.time() / 60, (time.time() - start) / 60))
    read()
    print('Done')

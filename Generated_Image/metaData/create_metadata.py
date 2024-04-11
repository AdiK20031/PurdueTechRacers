# -*- coding: utf-8 -*-
"""
Author: Thomas Wang 

Descripition: this script can ganerate metadata for picture set.
"""

import os
import csv
 
# This is some setting for the file path
PATH = "./renamed_data" # PATH indicate the storage location of the data set
METADATA_PATH = "./sign_metadata.csv" # where to store the metadata csv file 
extensions = ('.png')

with open(METADATA_PATH, 'w', newline='') as file:
     # decalre writing a file
     writer = csv.writer(file)
     writer.writerow(["fname", "label"])
     
     for filename in os.listdir(PATH):
         if filename.endswith( extensions ):
             label = ""
             fileNum=filename[0]

             print("filename:", filename)

            #find labels 
             for i in range(0,len(filename)):
                temp = filename.split("_",2)
                label = temp[0]+ "_" +temp[1]  
            
             writer.writerow([filename, label])
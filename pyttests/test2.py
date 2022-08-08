import csv

configs_path = r'/home/edulodi/videocoding/videos/classy.csv'
mylist = ['ui','laje',3,'classy']
with open(configs_path, 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(mylist)

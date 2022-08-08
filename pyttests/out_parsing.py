import csv

def parse_xpsnr_log(st,linenum):
    with open(st, 'rt') as output_text:
        out_string = output_text.readlines()
        for line in out_string:
            if (line.startswith("n")):
                if (int(line.split()[1]) == linenum+1):
                    print(line)
                    y_xpsnr = line.split()[4]
                    u_xpsnr = line.split()[7]
                    v_xpsnr = line.split()[10]
    return (y_xpsnr,u_xpsnr,v_xpsnr)

def parse_vmaf_log(file_path, linenum):
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if (row[0] == str((linenum))):
                vmaf = row[12]
    return (vmaf)
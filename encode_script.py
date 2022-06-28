import os
import csv
from csv import writer
import bjoontegaard_metric
import matplotlib.pyplot as plt

###############################GENERAL CONSTANTS##################################
YUV_PATH = "/home/edulodi/documents/videos"
FRAMES_AMNT = 5
##################################################################################

##################################LIBAOM AV1 CONSTANTS############################
LIBAOM_AV1_SAVES_PATH = "/home/edulodi/documents/LIBAOM_AV1_saved_rates.csv"
LIBAOM_AV1_PATH = "/home/edulodi/documents/aom/bin/aomenc"
##################################################################################

#######################SVT AV1 CONSTANTS##########################################
SVT_AV1_SAVES_PATH = "/home/edulodi/documents/SVT_AV1_saved_rates.csv"
SVT_AV1_PATH = "/home/edulodi/SVT_AV1/SVT-AV1/Bin/Release/SvtAv1EncApp"
##################################################################################

videos = os.listdir(YUV_PATH)
qps = [22, 27, 32, 37]
#qps = [22]

def parse_svt_output(pt1,pt2):
    BR_STRING = 'Total Frames	Average QP  	Y-PSNR   	U-PSNR   	V-PSNR		| 	Y-PSNR   	U-PSNR   	V-PSNR   	|	Y-SSIM   	U-SSIM   	V-SSIM   	|	Bitrate\n'
    with open(pt1, 'rt') as output_text:
        out_string = output_text.readlines()
        results_index = (out_string.index(BR_STRING) + 1)
        bitrate_string = out_string[results_index].split()[20]
        psnr_string = out_string[results_index].split()[2]
    with open(pt2, 'rt') as outtime_text:
        outtime_string = outtime_text.readlines()
    for strtime in outtime_string:
        if not strtime.startswith("Total Encoding Time"):
            continue
        timems_string = strtime.split()[3]
    return float(bitrate_string)*1024, float(psnr_string) , float(timems_string)

def parse_aom_output(st):
    with open(st, 'rt') as output_text:
        out_string = output_text.readlines()
        for line in out_string:
            if (line.startswith("Stream")):
                bitrateaom_string = line.split()[9]
                psnr_stringaom = line.split()[5]
                ms_stringaom = line.split()[11]
    return float(bitrateaom_string), float(psnr_stringaom), float(ms_stringaom)

def append_to_csv(csv_path, encoder, qp_value, video_name, psnr_value, br_value, time_ms):
    with open(csv_path, 'a') as (csv_list):
        writer_object = writer(csv_list)
        writer_object.writerow([encoder, qp_value, video_name, psnr_value, br_value,time_ms])

def csv_to_lists(csv_path, video_name): #returns 2 lists, the first one with the bitrates, and the second with the psnr
    bitters = []
    psnrers = []
    with open(csv_path, 'r') as csv_input:
        csv_reader = csv.reader(csv_input, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                if row != []:
                    if row[2] == video_name:
                        bitters.append(row[4])
                        psnrers.append(row[3])
            line_count += 1
    floats_bitters = [float(x) for x in bitters]
    floats_psnrers = [float(x) for x in psnrers]         
    return floats_bitters, floats_psnrers

for video in videos:
    if (".y4m" not in video) and (".yuv" not in video):
        continue

    yuv_full_path = "%s/%s" % (YUV_PATH, video)
    base_yuv_name = video.split("_")[0]

    for qp in qps:

        ##############################RODANDO SVT_AV1###########################################
        #output_path_svt = "/home/edulodi/SVT_AV1/output_svt/svt_saida_%s_qp%s.txt" % (base_yuv_name, qp)
        #output_path_svt_time = "/home/edulodi/SVT_AV1/output_svt/svt_time_saida_%s_qp%s.txt" % (base_yuv_name, qp)
        #svt_parameters = " -i %s -n %i" % (yuv_full_path, FRAMES_AMNT)
        #svt_parameters += " --enable-stat-report 1 --stat-file %s --lp 1" % (output_path_svt)
        #svt_parameters += " --qp %s --max-qp %s --min-qp %s --rc 0" % (qp,qp,qp)
        #encode_cmd_svt = "%s %s 2> %s" % (SVT_AV1_PATH, svt_parameters, output_path_svt_time)
        #print(encode_cmd_svt)
        #os.system(encode_cmd_svt)
        #br_svt, psnr_svt, timems_svt = parse_svt_output(output_path_svt, output_path_svt_time)
        #append_to_csv(SVT_AV1_SAVES_PATH, 'SVT', qp, base_yuv_name, psnr_svt, br_svt, timems_svt)
        ########################################################################################

        ##############################RODANDO LIBAOM_AV1############################################
        output_path_libaom = "/home/edulodi/documents/output_aom/aom_saida_%s_qp%s.txt" % (base_yuv_name,qp)
        aom_parameters = " --limit=%i --verbose --cq-level=%s --cpu-used=1" % (FRAMES_AMNT, qp)
        aom_parameters += " -o /home/edulodi/documents/output_aom/aom_vid_saida_%s_qp%s.webm %s" % (base_yuv_name,qp, yuv_full_path)
        encode_cmd_aom = "%s %s > %s 2>&1 " % (LIBAOM_AV1_PATH, aom_parameters, output_path_libaom)
        print(encode_cmd_aom)
        os.system(encode_cmd_aom)
        br_aom, psnr_aom, timems_aom = parse_aom_output(output_path_libaom)
        append_to_csv(LIBAOM_AV1_SAVES_PATH, 'AOM', qp, base_yuv_name, psnr_aom, br_aom, timems_aom)
        ########################################################################################

#br_foreman_svt , psnr_foreman_svt = csv_to_lists(SVT_AV1_SAVES_PATH,"foreman")
#br_akiyo_svt , psnr_akiyo_svt = csv_to_lists(SVT_AV1_SAVES_PATH,"akiyo")
#br_flower_svt , psnr_flower_svt = csv_to_lists(SVT_AV1_SAVES_PATH,"flower")
#br_carphone_svt , psnr_carphone_svt = csv_to_lists(SVT_AV1_SAVES_PATH,"carphone")
#br_foreman_aom , psnr_foreman_aom = csv_to_lists(LIBAOM_AV1_SAVES_PATH,"foreman")
#br_akiyo_aom , psnr_akiyo_aom = csv_to_lists(LIBAOM_AV1_SAVES_PATH,"akiyo")
#br_flower_aom , psnr_flower_aom = csv_to_lists(LIBAOM_AV1_SAVES_PATH,"flower")
#br_carphone_aom , psnr_carphone_aom = csv_to_lists(LIBAOM_AV1_SAVES_PATH,"carphone")
#
#print(br_foreman_svt,"\n",psnr_foreman_svt,"\n",br_foreman_aom,"\n",psnr_foreman_aom)
#
#bd_rate_foreman = bjoontegaard_metric.BD_PSNR(br_foreman_svt,psnr_foreman_svt,br_foreman_aom,psnr_foreman_aom)
#bd_rate_akiyo = bjoontegaard_metric.BD_PSNR(br_akiyo_svt,psnr_akiyo_svt,br_akiyo_aom,psnr_akiyo_aom)
#bd_rate_flower = bjoontegaard_metric.BD_PSNR(br_flower_svt , psnr_flower_svt,br_flower_aom , psnr_flower_aom)
#bd_rate_carphone = bjoontegaard_metric.BD_PSNR(br_carphone_svt , psnr_carphone_svt,br_carphone_aom , psnr_carphone_aom)
#
#print(bd_rate_foreman, bd_rate_akiyo, bd_rate_flower, bd_rate_carphone)

#########################plotting###############################
#x = ["foreman","akiyo","flower","carphone"]
#y = [bd_rate_foreman, bd_rate_akiyo, bd_rate_flower, bd_rate_carphone]
#
#plt.plot(x,y)
#plt.xlabel("QPs")
#plt.ylabel("BD")
#plt.title("BD_RATE AV1 - AOM x SVT")
#plt.show()

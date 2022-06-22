import os
import csv
from csv import writer
import bjoontegaard_metric

###############################GENERAL CONSTANTS##################################
YUV_PATH = "/home/edulodi/documents/videos"
FRAMES_AMNT = 2
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
#qps = [22, 27, 32, 37]
qps = [22]


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
        for s in out_string:
            if s.startswith("Stream"):
                continue
        bitrate_string = s.split()[9]
        psnr_string = s.split()[5]
        ms_string = s.split()[11]
    return float(bitrate_string), float(psnr_string), float(ms_string)

def append_to_csv(csv_path, encoder, qp_value, video_name, psnr_value, br_value, time_ms):
    with open(csv_path, 'a') as (csv_list):
        writer_object = writer(csv_list)
        writer_object.writerow([encoder, qp_value, video_name, psnr_value, br_value,time_ms])

def csv_to_lists(csv_path): #returns 2 lists, the first one with the bitrates, and the second with the psnr
    bitters = []
    psnrers = []
    with open(csv_path, 'r') as csv_input:
        csv_reader = csv.reader(csv_input, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                bitters.append(row[4])
                psnrers.append(row[3])
            line_count += 1
    return bitters, psnrers

for video in videos:
    if (".y4m" not in video) and (".yuv" not in video):
        continue

    yuv_full_path = "%s/%s" % (YUV_PATH, video)
    base_yuv_name = video.split("_")[0]

    for qp in qps:
        ##############################RODANDO LIBAOM_AV1############################################
        output_path_libaom = "/home/edulodi/documents/output_aom/aom_saida_%s_qp%s.txt" % (base_yuv_name,qp)
        aom_parameters = " limit=%s --tune=psnr --psnr" % (FRAMES_AMNT)
        aom_parameters = " -o /home/edulodi/documents/output_aom/aom_vid_saida_%s_qp%s.webm %s" % (base_yuv_name,qp, yuv_full_path)
        encode_cmd_aom = "%s %s &> %s" % (LIBAOM_AV1_PATH, aom_parameters, output_path_libaom)
        os.system(encode_cmd_aom)
        br_aom, psnr_aom, timems_aom = parse_aom_output(output_path_libaom)
        append_to_csv(LIBAOM_AV1_SAVES_PATH, 'AOM', qp, base_yuv_name, psnr_aom, br_aom, timems_aom)
        ########################################################################################

        ##############################RODANDO SVT_AV1###########################################
        output_path_svt = "/home/edulodi/SVT_AV1/output_files/svt_saida_%s_qp%d.txt" % (base_yuv_name, qp)
        output_path_svt_time = "/home/edulodi/SVT_AV1/output_files/svt_time_saida_%s_qp%d.txt" % (base_yuv_name, qp)
        svt_parameters = " -i %s -n %i" % (yuv_full_path, FRAMES_AMNT)
        svt_parameters += " --enable-stat-report 1 --stat-file %s --lp 1" % (output_path_svt)
        svt_parameters += " --qp %d --max-qp %d --min-qp %d --rc 0" % (qp,qp,qp)
        encode_cmd_svt = "%s %s" % (SVT_AV1_PATH, svt_parameters)
        print(encode_cmd_svt)
        os.system(encode_cmd_svt)
        br_svt, psnr_svt, timems_svt = parse_svt_output(output_path_svt, output_path_svt_time)
        append_to_csv(SVT_AV1_SAVES_PATH, 'SVT', qp, base_yuv_name, psnr_svt, br_svt, timems_svt)
        ########################################################################################
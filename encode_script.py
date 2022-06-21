import os
import csv
from csv import writer

###############################GENERAL CONSTANTS##################################
YUV_PATH = "/home/edulodi/documents/videos"
FRAMES_AMNT = 2
##################################################################################
##########################VTM CONSTANTS##########################################
VTM_PATH = "/home/edulodi/documents/VTM17.0/VVCSoftware_VTM-VTM-17.0/bin/EncoderAppStatic"
VTM_CFG_PATH = "/home/edulodi/documents/VTM17.0/VVCSoftware_VTM-VTM-17.0/cfg"
VTM_SAVES_PATH = "/home/edulodi/documents/VTM_saved_rates.csv"
##################################################################################
#######################AV1 CONSTANTS##############################################
AV1_SAVES_PATH = "/home/edulodi/documents/AV1_saved_rates.csv"
SVT_AV1_PATH = "/home/edulodi/SVT_AV1/SVT-AV1/Bin/Release/SvtAv1EncApp"
##################################################################################

videos = os.listdir(YUV_PATH)
#qps = [22, 27, 32, 37]
qps = [22]
def parse_vtm_output(pt):
    BR_STRING = "\tTotal Frames |  Bitrate      Y-PSNR   U-PSNR   V-PSNR   YUV-PSNR \n"
    with open(pt, 'rt') as output_text:
        out_string = output_text.readlines()
        results_index = (out_string.index(BR_STRING) + 1)
        bitrate_string = out_string[results_index].split()[2]
        psnr_string = out_string[results_index].split()[6]
    return (float(bitrate_string), float(psnr_string))

def parse_av1_output(pt):
    BR_STRING = 'Total Frames	Average QP  	Y-PSNR   	U-PSNR   	V-PSNR		| 	Y-PSNR   	U-PSNR   	V-PSNR   	|	Y-SSIM   	U-SSIM   	V-SSIM   	|	Bitrate\n'
    with open("akio.txt", 'rt') as output_text:
        out_string = output_text.readlines()
        results_index = (out_string.index(BR_STRING) + 1)
        bitrate_string = out_string[results_index].split()[20]
        psnr_string = out_string[results_index].split()[2]
    return float(bitrate_string)*1024, float(psnr_string)

def append_to_csv(csv_path, encoder, qp_value, video_name, psnr_value, br_value):
    with open(csv_path, 'a') as (csv_list):
        writer_object = writer(csv_list)
        writer_object.writerow([encoder, qp_value, video_name, psnr_value, br_value])

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
    
    yuv_full_path = "%s/%s" % (YUV_PATH, video)
    base_yuv_name = video.split("_")[0]

    for qp in qps:
        ##############################RODANDO VTM############################################
        output_path_vtm = "vtm_saida_%s_qp%d.txt" % (base_yuv_name, qp)
        vtm_parameters = "-c %s/encoder_randomaccess_vtm.cfg " % (VTM_CFG_PATH)
        vtm_parameters += "-c %s/per-sequence/%s.cfg " % (VTM_CFG_PATH, base_yuv_name)
        vtm_parameters += "--InputFile=%s " %(yuv_full_path)
        vtm_parameters += "--QP=%d -f %i" % (qp,FRAMES_AMNT)
        vtm_parameters += "--BitstreamFile=%s_qp%d.bin " % (base_yuv_name, qp)
        encode_cmd_vtm = "%s %s > %s" % (VTM_PATH, vtm_parameters, output_path_vtm)
        os.system(encode_cmd_vtm)
        br_vtm, psnr_vtm = parse_vtm_output(output_path_vtm)
        print (br_vtm, psnr_vtm)
        append_to_csv(VTM_SAVES_PATH, 'VTM', qp, base_yuv_name, psnr_vtm, br_vtm)
        ########################################################################################

        ##############################RODANDO SVT_AV1###########################################
        output_path_av1 = "/home/edulodi/SVT_AV1/output_files/av1_saida_%s_qp%d.txt" % (base_yuv_name, qp)
        av1_parameters = "-i %s -n %i --enable-stat-report 1 --stat-file %s --qp %d --max-qp %d --min-qp %d --rc 0" % (yuv_full_path, FRAMES_AMNT, output_path_av1, qp, qp, qp)
        encode_cmd_av1 = "%s %s" % (SVT_AV1_PATH, av1_parameters)
        os.system(encode_cmd_av1)
        br_av1, psnr_av1 = parse_av1_output(output_path_av1)
        append_to_csv(AV1_SAVES_PATH, 'AV1', qp, base_yuv_name, psnr_av1, br_av1)
        #######################################################################################

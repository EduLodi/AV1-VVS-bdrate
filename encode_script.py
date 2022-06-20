import os
import csv
from csv import writer

YUV_PATH = "./videos"
VTM_PATH = "./VTM17.0/VVCSoftware_VTM-VTM-17.0/bin/EncoderAppStatic"
VTM_CFG_PATH = "./VTM17.0/VVCSoftware_VTM-VTM-17.0/cfg"
VTM_SAVES_PATH = "VTM_saved_rates.csv"
AV1_SAVES_PATH = "/home/edulodi/documents/AV1_saved_rates.csv"
BR_STRING = "\tTotal Frames |  Bitrate      Y-PSNR   U-PSNR   V-PSNR   YUV-PSNR \n"
FRAMES_AMNT = 2

videos = os.listdir(YUV_PATH)
#qps = [22, 27, 32, 37]
qps = [22]
def parse_vtm_output(pt):
    with open(pt, 'rt') as output_text:
        out_string = output_text.readlines()
        results_index = (out_string.index(BR_STRING) + 1)
        bitrate_string = out_string[results_index].split()[2]
        psnr_string = out_string[results_index].split()[6]
    return (float(bitrate_string), float(psnr_string))

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
    
    base_yuv_name = video.split("_")[0]
    yuv_full_path = "%s/%s" % (YUV_PATH, video)
    
    for qp in qps:
        
        ##############################RODANDO VTM############################################
        output_path = "saida_%s_qp%d.txt" % (base_yuv_name, qp)
        vtm_parameters = "-c %s/encoder_randomaccess_vtm.cfg " % (VTM_CFG_PATH)
        vtm_parameters += "-c %s/per-sequence/%s.cfg " % (VTM_CFG_PATH, base_yuv_name)
        vtm_parameters += "--InputFile=%s " %(yuv_full_path)
        vtm_parameters += "--QP=%d -f %i" % (qp,FRAMES_AMNT)
        vtm_parameters += "--BitstreamFile=%s_qp%d.bin " % (base_yuv_name, qp)
        encode_cmd = "%s %s > %s" % (VTM_PATH, vtm_parameters, output_path)
       # print(encode_cmd)
       # os.system(encode_cmd)
        br_vtm, psnr_vtm = parse_vtm_output(output_path)
        print (br_vtm, psnr_vtm)
        append_to_csv(VTM_SAVES_PATH, 'VTM', qp, base_yuv_name, psnr_vtm, br_vtm)
        ########################################################################################

        

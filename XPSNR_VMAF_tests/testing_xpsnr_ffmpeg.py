import os
import csv
import out_parsing

FFMPEG_PATH = '~/ffmpeg/ffmpeg'
PATH_VIDEO1 = '~/video-coding/VIDEOS2/bowing_pair/bowing_cif.y4m'
PATH_VIDEO2 = '~/video-coding/VIDEOS2/bowing_pair/bowing_aomdec.y4m'
OUTPUT_XPSNR_PATH = '/home/edulodi/video-coding/VIDEOS2/bowing_pair/xpsnr.log'
OUTPUT_VMAF_PATH = '/home/edulodi/video-coding/VIDEOS2/bowing_pair/vmaf.csv'
VMAF_PATH = '~/vmaf/vmaf'
CSV_OUT_PATH = 'XPSNR_VMAF_tests/frames_metrics.csv'
frame_number = 300

def xpsnr_creator(videoref, videodis, output):
    os.system("ffmpeg" + " -i " + videoref + " -i " + videodis + ' -lavfi xpsnr="stats_file=' + output + '" -f null -')

def vmaf_creator(videoref, videodis, output):
    os_cmd = "vmaf -r " + videoref + " -d " + videodis + " -o " + OUTPUT_VMAF_PATH + "vmaf.csv --csv"
    os.system(os_cmd)

#vmaf_creator(PATH_VIDEO1,PATH_VIDEO2,OUTPUT_VMAF_PATH)
#xpsnr_creator(PATH_VIDEO1,PATH_VIDEO2,OUTPUT_XPSNR_PATH)

with open(CSV_OUT_PATH, mode='w') as metrics_file:
    metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    metrics_writer.writerow(['Frame', 'VMAF', 'Y_XPSNR', 'U_PSNR', 'V_PSNR'])

for frame in range(frame_number):
    vmaf = out_parsing.parse_vmaf_log(OUTPUT_VMAF_PATH,frame)
    yxpsnr, uxpsnr, vxpsnr = out_parsing.parse_xpsnr_log(OUTPUT_XPSNR_PATH,frame)
    with open(CSV_OUT_PATH, mode='a') as metrics_file:
        metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        metrics_writer.writerow([frame,vmaf,yxpsnr,uxpsnr,vxpsnr])
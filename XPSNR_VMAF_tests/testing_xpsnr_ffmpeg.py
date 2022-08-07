import os
import csv
import out_parsing
import configparser

config = configparser.ConfigParser()
config.read(r'/home/edulodi/videocoding/AV1-VVS-bdrate/XPSNR_VMAF_tests/configs.ini')
FFMPEG_PATH = config.get('paths', 'ffmpeg')
PATH_VIDEO1 = config.get('paths', 'video1path')
PATH_VIDEO2 = config.get('paths', 'video2path')
OUTPUT_XPSNR_PATH = config.get('paths', 'xpsnrout')
OUTPUT_VMAF_PATH = config.get('paths', 'vmafout')
CSV_OUT_PATH = 'XPSNR_VMAF_tests/frames_metrics_svt.csv'
frame_number = 300
print(FFMPEG_PATH)

#def xpsnr_creator(videoref, videodis, output):
#    os.system(FFMPEG_PATH + " -i " + videoref + " -i " + videodis + ' -lavfi xpsnr="stats_file=' + output + '" -f null -')
#
#def vmaf_creator(videoref, videodis, output):
#    os_cmd = "vmaf -r " + videoref + " -d " + videodis + " -o " + OUTPUT_VMAF_PATH +  " --csv"
#    os.system(os_cmd)
#
#xpsnr_creator(PATH_VIDEO1,PATH_VIDEO2,OUTPUT_XPSNR_PATH)
#
#vmaf_creator(PATH_VIDEO1,PATH_VIDEO2,OUTPUT_VMAF_PATH)
#
#with open(CSV_OUT_PATH, mode='w') as metrics_file:
#    metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    metrics_writer.writerow(['Frame', 'VMAF', 'Y_XPSNR', 'U_PSNR', 'V_PSNR'])
#
#for frame in range(frame_number):
#    vmaf = out_parsing.parse_vmaf_log(OUTPUT_VMAF_PATH,frame)
#    yxpsnr, uxpsnr, vxpsnr = out_parsing.parse_xpsnr_log(OUTPUT_XPSNR_PATH,frame)
#    with open(CSV_OUT_PATH, mode='a') as metrics_file:
#        metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#        metrics_writer.writerow([frame,vmaf,yxpsnr,uxpsnr,vxpsnr])
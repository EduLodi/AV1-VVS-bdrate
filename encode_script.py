import os

YUV_PATH = "./videos"
VTM_PATH = "./VTM17.0/VVCSoftware_VTM-VTM-17.0/bin/EncoderAppStatic"
VTM_CFG_PATH = "./VTM17.0/VVCSoftware_VTM-VTM-17.0/cfg"
SAVES_PATH = "saved_rates"
BR_STRING = "\tTotal Frames |  Bitrate      Y-PSNR   U-PSNR   V-PSNR   YUV-PSNR \n"

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


for video in videos:
    for qp in qps:
        base_yuv_name = video.split("_")[0]
        yuv_full_path = "%s/%s" % (YUV_PATH, video)
        output_path = "saida_%s_qp%d.txt" % (base_yuv_name, qp)
        vtm_parameters = "-c %s/encoder_randomaccess_vtm.cfg " % (VTM_CFG_PATH)
        vtm_parameters += "-c %s/per-sequence/%s.cfg " % (VTM_CFG_PATH, base_yuv_name)
        vtm_parameters += "--InputFile=%s " %(yuv_full_path)
        vtm_parameters += "--QP=%d -f 2" % (qp)
        vtm_parameters += "--BitstreamFile=%s_qp%d.bin " % (base_yuv_name, qp)
        encode_cmd = "%s %s > %s" % (VTM_PATH, vtm_parameters, output_path)
       # print(encode_cmd)
       # os.system(encode_cmd)
        br, psnr = parse_vtm_output(output_path)
        print (br, psnr)
        with open(SAVES_PATH, 'w') as saves_list:
           saves_list.write("%s,%s.PSNR: %f\n" % (str(qp), base_yuv_name, psnr))
           saves_list.write("%s,%s.BITRATE: %f\n" % (str(qp), base_yuv_name, br))
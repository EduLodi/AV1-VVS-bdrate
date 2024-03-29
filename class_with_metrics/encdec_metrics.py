import configparser
import csv
import os
import class_with_metrics.metrics_outparse as metrics_outparse
class AV1Enc:

    #init method, the rawvideo is a y4m file, the configs file is in the same directory as script
    def __init__(self, rawvideo, configs):
        global fconfig
        fconfig = configparser.ConfigParser()
        fconfig.read(configs)
        self.raw = rawvideo

    #the SVT method, it encodes, decodes, and compares the two videos using the availabe metrics, the results are put together into a csv file 
    def svt_encdec(self):
        svtpath = fconfig.get('paths', 'svtav1enc')
        options_svte = fconfig.get('svt_ops', 'svt_enc_options')
        encoded_out = fconfig.get('paths','svt_encoded_path')
        cmdline = (svtpath + ' ' + options_svte + ' -i ' + self.raw + ' -b ' + encoded_out)
        print(cmdline)
        os.system(cmdline)
        svtpath = fconfig.get('paths','svtav1dec')
        options_svtd = fconfig.get('svt_ops', 'svt_dec_options')
        decoded_out = fconfig.get('paths','svt_decoded_path')
        cmdline = (svtpath + ' ' + options_svtd + ' -i ' + encoded_out + ' -o ' + decoded_out)
        print(cmdline)
        os.system(cmdline)
        y4m_path = fconfig.get('paths', 'svt_y4m_path')
        self.yuvtoy4m(decoded_out,y4m_path)
        outxpsnr = fconfig.get('paths','svtxpsnrout')
        self.xpsnr(y4m_path,outxpsnr)
        outvmaf = fconfig.get('paths','svtvmafout')
        self.vmaf(y4m_path,outvmaf)
        frames = int(fconfig.get('video_presets','nof_frames'))
        outmetricscsv = fconfig.get('paths','svt_metricscsv')
        self.metrics_csv(outmetricscsv,outvmaf,outxpsnr,frames)

    #the libaom method, does the same as the SVT one, the only difference being that the decoded aom output is already Y4M, so it doesn't need the yuvtoy4m method
    def aomencdec(self):
        aompath = fconfig.get('paths', 'libaomenc')
        options_aome = fconfig.get('aom_ops', 'aom_enc_options')
        encoded_out = fconfig.get('paths','aom_encoded_path')
        cmdline = (aompath + ' ' + options_aome + ' -o ' + encoded_out + ' ' + self.raw)
        os.system(cmdline)
        aompath = fconfig.get('paths','libaomdec')
        options_aomd = fconfig.get('aom_ops', 'aom_dec_options')
        decoded_out = fconfig.get('paths','aom_decoded_path')
        cmdline = (aompath + ' ' + options_aomd + ' ' + encoded_out + ' -o ' + decoded_out)
        os.system(cmdline)
        outxpsnr = fconfig.get('paths','aomxpsnrout')
        self.xpsnr(decoded_out,outxpsnr)
        outvmaf = fconfig.get('paths','aomvmafout')
        self.vmaf(decoded_out,outvmaf)
        frames = int(fconfig.get('video_presets','nof_frames'))
        outmetricscsv = fconfig.get('paths','aom_metricscsv')
        self.metrics_csv(outmetricscsv,outvmaf,outxpsnr,frames)

    #transforms yuv into y4m, the yuv specs need to be in the config file
    def yuvtoy4m(self,input,output):
        ffmpegpath = fconfig.get('paths','ffmpeg')
        input_path = input
        output_path = output
        width = fconfig.get('video_presets','width')
        height = fconfig.get('video_presets','height')
        frate = fconfig.get('video_presets', 'frame_rate')
        pfmt = fconfig.get('video_presets', 'pix_fmt')
        cmdline = ffmpegpath + ' -f rawvideo -vcodec rawvideo -s ' + width + 'x' + height + ' -r ' + frate + ' -pix_fmt ' + pfmt
        cmdline += ' -i ' +  input_path + ' ' + output_path + ' -y'
        print(cmdline)
        os.system(cmdline)

    #computes xpsnr using ffmpeg
    def xpsnr(self, y4m_decoded, out_xpsnr):
        videoref = self.raw
        videodis = y4m_decoded
        ffmpegpath = fconfig.get('paths','ffmpeg')
        output = out_xpsnr
        cmdline = ffmpegpath + " -i " + videoref + " -i " + videodis + ' -lavfi xpsnr="stats_file=' + output + '" -f null -'
        print(cmdline)
        os.system(cmdline)

    #computes vmaf
    def vmaf(self, y4m_decoded, out_vmaf):
        videoref = self.raw
        videodis = y4m_decoded
        vmafpath = fconfig.get('paths','vmaf')
        output = out_vmaf
        cmdline = vmafpath + " -r " + videoref + " -d " + videodis + " -o " + output +  " --csv"
        print(cmdline)
        os.system(cmdline)

    #puts the results from the previous calculated metrics into a single csv file
    def metrics_csv(self, outputcsv, inputvmaf, inputxpsnr, frames):
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['Frame', 'VMAF', 'Y_XPSNR', 'U_PSNR', 'V_PSNR'])
        for frame in range(frames):
            vmaf = metrics_outparse.parse_vmaf_log(inputvmaf,frame)
            yxpsnr, uxpsnr, vxpsnr = metrics_outparse.parse_xpsnr_log(inputxpsnr,frame)
            with open(outputcsv, mode='a') as metrics_file:
                metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                metrics_writer.writerow([frame,vmaf,yxpsnr,uxpsnr,vxpsnr])

bowing_path = '/home/edulodi/videocoding/videos/small_bowing.y4m'
configs_path = 'class_with_metrics/configs.ini'

bowing = AV1Enc(bowing_path, configs_path)
bowing.aomencdec()
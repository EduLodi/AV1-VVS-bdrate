import configparser
import os
class AV1Enc:

    def __init__(self, rawvideo, configs):
        global fconfig
        fconfig = configparser.ConfigParser()
        fconfig.read(configs)
        self.raw = rawvideo

    def svt_encdec(self):
        svtpath = fconfig.get('paths', 'svtav1enc')
        options_svte = fconfig.get('svt_ops', 'svt_enc_options')
        encoded_out = fconfig.get('paths','svt_encoded_path')
        cmdline = (svtpath + ' ' + options_svte + ' -i ' + self.raw + ' -b ' + encoded_out)
        print(cmdline)
        #os.system(cmdline)
        svtpath = fconfig.get('paths','svtav1dec')
        options_svtd = fconfig.get('svt_ops', 'svt_dec_options')
        decoded_out = fconfig.get('paths','svt_decoded_path')
        cmdline = (svtpath + ' ' + options_svtd + ' -i ' + encoded_out + ' -o ' + decoded_out)
        print(cmdline)
        y4m_path = fconfig.get('paths', 'svt_y4m_path')
        self.yuvtoy4m(decoded_out,y4m_path)

    def yuvtoy4m(self,input,output):
        ffmpegpath = fconfig.get('paths','ffmpeg')
        input_path = input
        output_path = output
        width = fconfig.get('video_presets','width')
        height = fconfig.get('video_presets','height')
        frate = fconfig.get('video_presets', 'frame_rate')
        pfmt = fconfig.get('video_presets', 'pix_fmt')
        cmdline = ffmpegpath + ' -f rawvidedo -vcodec rawvideo -s ' + width + 'x' + height + ' -r ' + frate + ' -pix_fmt ' + pfmt
        cmdline += ' -i ' +  input_path + ' ' + output_path
        print(cmdline)


bowing_path = '~/videocoding/videos/bowing_cif.y4m'
configs_path = '/home/edulodi/videocoding/AV1-VVS-bdrate/XPSNR_VMAF_tests/configs.ini'

bowing = AV1Enc(bowing_path, configs_path)
bowing.svt_encdec()
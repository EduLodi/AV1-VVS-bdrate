import configparser

configs_path = r'/home/edulodi/videocoding/AV1-VVS-bdrate/XPSNR_VMAF_tests/configs.ini'

config = configparser.ConfigParser()
config.read(configs_path)
print(config.get('paths', 'ffmpeg'))

class laje():
    
    def __init__(self, raw_video, configs):
        global config
        config = configparser.ConfigParser()
        config.read(configs)
        self.raw = raw_video
    
    def hehe(self):
        self.super = ('super nintendo' + self.raw)
        print(self.super)
        print(config.get('paths', 'ffmpeg'))

x = laje('uiui', configs_path)
x.hehe()


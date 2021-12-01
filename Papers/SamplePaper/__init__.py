def SampleRes(url):
    return 'SampleRes: '+url

def main(PaperLib):
    PaperLib.bind('SamplePaper',SampleRes)
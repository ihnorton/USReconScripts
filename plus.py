import sys, os
import subprocess
import numpy as np
from mhaio import *

PLUS_PATH = "F:/neuro_ultrasound/software/PlusExperimental-bin-06192013/bin/Release/"
PLUS_ENV = os.environ
PLUS_ENV["PATH"] = PLUS_PATH+os.path.pathsep+PLUS_ENV["PATH"]

SP_INFO = subprocess.STARTUPINFO()
SP_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW

DEFAULT_TRANSFORM = "ImageToTracker"

anonymize_regions = {
    "1280x1024": ["0", "0", "1280", "1024"],
    "1920x1080": ["550", "0", "590", "60"],
    }
    
config_files = {
    "1280x1024": "AMIGO_BrainLab_1280x1024_offset_cal.xml",
    "1920x1080": "AMIGO_BrainLab_1920x1080_offset_cal.xml"
    }
config_path = "Z:/Ultrasound/scripts/config"

def call_out(*args, **kwargs):
    p = subprocess.Popen(*args, stdout=subprocess.PIPE, env=PLUS_ENV,
                         startupinfo=SP_INFO, **kwargs)
    return p.communicate()

def get_slice_dims(seq_file):
    hdr = parse_mha_header(open(seq_file))
    dims = np.array(hdr["DimSize"].split(), np.long)
    slicedim = dims[0:2]
    return slicedim
    
def anonymize_sequence(seq_file, region, output_file = None):
    if (output_file == None):
        output_file = "anon-"+seq_file
    # Need to use full path so PLUS doesn't default to bin/
    output_file = os.path.join(os.getcwd(), output_file)
    res,err = call_out(
        ["EditSeqMetaFile",
        "--operation=FILL_IMAGE_RECTANGLE",
        "--source-seq-file=%s" % seq_file,
        "--output-seq-file=%s" % output_file,
        "--rect-origin", region[0], region[1],
        "--rect-size", region[2], region[3]
        ])
    if (res.count("successful") < 1):
        print(res)

def auto_anonymize(sequences):
    for seq_file in sequences:
        slicedim = get_slice_dims(seq_file)
        dimname = str(slicedim[0])+"x"+str(slicedim[1])
        
        anonymize_sequence(seq_file, anonymize_regions[dimname])

def reconstruct_sequence(seq_file, config_file, transform, output_file = None):
    if (output_file == None):
        output_file = "recon-"+seq_file
    output_file = os.path.join(os.getcwd(), output_file)
    res,err = call_out(["VolumeReconstructor",
          "--config-file=%s" % config_file,
          "--img-seq-file=%s" % seq_file,
          "--output-volume-file=%s" % output_file,
          "--transform=%s" % transform])
    print(res)
          
def auto_recon(sequences, transform=DEFAULT_TRANSFORM):
    for seq_file in sequences:
        slicedim = get_slice_dims(seq_file)
        dimname = str(slicedim[0])+"x"+str(slicedim[1])
        
        config_file = os.path.join(config_path, config_files[dimname])
        reconstruct_sequence(seq_file, config_file, transform)
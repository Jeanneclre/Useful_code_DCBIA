import SimpleITK as sitk
import numpy as np
from utils import ResampleImage,CheckSharedList
import os, glob, argparse
import multiprocessing as mp
import numpy as np
from pathlib import Path

def CenterImage(scan_path, out_path):
    img = sitk.ReadImage(scan_path)
    # Translation
    img.SetOrigin((0, 0, 0))

    center_T= -np.array(img.GetSize())/2.0
    print('T1:',center_T, 'outpath:',out_path)
    T = np.array(img.TransformContinuousIndexToPhysicalPoint(center_T))
    print('T:',T)
    translation = sitk.TranslationTransform(3)
    translation.SetOffset(T)
    print('translation:',translation)

    img.SetOrigin(T)  # Update the origin
    sitk.WriteImage(img, out_path)

def ListFiles(input_path):
    files = []
    normpath = os.path.normpath("/".join([input_path, '**', '']))
    for file in sorted(glob.iglob(normpath, recursive=True)):
        if os.path.isfile(file) and True in [ext in file for ext in [".nrrd", ".nii", ".nii.gz", 'gipl.gz']]:
            files.append(file)
    return files

def CenterBatch(out_dir,files,shared_list,num_worker):
    
    for file in files:
        path_obj = Path(file)
        new_parts = path_obj.parts[2:] if path_obj.is_absolute() else path_obj.parts[1:]
        # Join the components back to form the new path
        new_path = Path(*new_parts)
        outpath = os.path.join(out_dir,new_path)
        print('outpath:',outpath)

        # rename the file by adding 'centered' at the end of the name
        outpath = outpath.replace('.nii.gz','_centered.nii.gz')
        # keep just the filename
        filename = os.path.basename(outpath)
        # remove the filename from the path
        outpath = outpath.replace(filename,'')
        if not os.path.exists(os.path.dirname(outpath)):
            os.makedirs(outpath)
            CenterImage(file,os.path.join(outpath,filename))
            shared_list[num_worker] += 1


def main(args):
    out_dir = args.out_dir
    nb_worker = args.nb_proc

    nb_scan_done=0
    files = ListFiles(args.data_dir)
    if out_dir == '':
        out_dir = os.path.join(args.data_dir,'Output')

    if not os.path.exists(out_dir):
        # create a directory named out_dir
        os.makedirs(out_dir)

  
    for file in files:
        outpath= ''
        print("file:",file)
        path_obj = Path(file)
        new_parts = path_obj.parts[2:] if path_obj.is_absolute() else path_obj.parts[1:]
        # Join the components back to form the new path
        new_path = Path(*new_parts)
        outpath = os.path.join(out_dir,new_path)
        
        # rename the file by adding 'centered' at the end of the name
        outpath = outpath.replace('.nii.gz','_centered.nii.gz')
        # keep just the filename
        filename = os.path.basename(outpath)
        
        # remove the filename from the path
        outpath = outpath.replace(filename,'')
        print('outpath:',outpath)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        CenterImage(file,os.path.join(outpath,filename))
        nb_scan_done +=1
   


    print(nb_scan_done) 

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',help='directory where json files to merge are',type=str,default='./')#'/home/luciacev/Desktop/Luc_Anchling/DATA/ASO_CBCT/NotOriented/Anonymized')#required=True)
    parser.add_argument('--out_dir',help='directory where json files to merge are',type=str,default='./')
    parser.add_argument('--nb_proc',help='number of processes to use for computation',type=int,default=5)
    args = parser.parse_args() 
    main(args)
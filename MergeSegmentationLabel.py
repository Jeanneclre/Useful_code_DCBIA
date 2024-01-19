import SimpleITK as sitk
import numpy as np
from DCMConvert import search
import os
import multiprocessing as mp
from pathlib import Path

def merge_labels(files,input_dir,out_dir):
    for file in files:
        print('file:',file)
        if file.endswith(".nii.gz"):
            seg = sitk.ReadImage(file)
            array = sitk.GetArrayFromImage(seg)
            array = np.where(array > 0,1,0)
            segtrans = sitk.GetImageFromArray(array)
            segtrans.CopyInformation(seg)

            path_obj = Path(file)
            new_parts = path_obj.parts[2:] if path_obj.is_absolute() else path_obj.parts[1:]
            # Join the components back to form the new path
            new_path = Path(*new_parts)
            outname = os.path.join(out_dir,new_path)

            filename = os.path.basename(outname)
            output_directory = outname.replace(filename,'')
            print('outname:',outname)
            if not os.path.exists(output_directory):
                os.makedirs(os.path.dirname(output_directory))

            output_file_path = os.path.join(output_directory, filename.replace('.nii.gz', '_merged.nii.gz'))
            sitk.WriteImage(sitk.Cast(segtrans,sitk.sitkUInt16),output_file_path)

if __name__ == "__main__":
        
        data_dir = "./02_Centered/Segs_Non_Oriented/Seg_Controls_per_patients/"
        out_dir = "./02_Centered_Merged/"
        
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    
        files = search(data_dir,".nii.gz")[".nii.gz"]
    
        merge_labels(files,data_dir,out_dir)

        # splits = np.array_split(files,20)
    
        # processes = [mp.Process(target=merge_labels, args=(split,data_dir,out_dir)) for split in splits]
    
        # for p in processes:
        #     p.start()
        # for p in processes:
        #     p.join()

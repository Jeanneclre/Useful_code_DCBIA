import nibabel as nib

# Load the NIFTI image
img = nib.load('r_127_T1_Right_seg_or.nii.gz')

# Access its header
header = img.header
# Set quaternion values to represent no rotation
header.set_qform(header.get_sform(), code=1)  # This sets qform to be the same as sform

# Modify quaternion values
header['quatern_b'] = 0.0
header['quatern_c'] = 0.0
header['quatern_d'] = 1.0

# Save the modified image
nib.save(img, 'r_127_T1_Right_seg_or_MOD3.nii.gz')

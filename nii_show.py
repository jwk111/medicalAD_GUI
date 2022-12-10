import nibabel as nib
from nibabel.viewers import OrthoSlicer3D
import argparse


def main(args):
    img=nib.load(args.nii_path)
    # img2 = nib.load('ADNI_result/I131842_brain.nii.gz')
    # img3 = nib.load("ADNI_result/I131842.nii.gz")
    # 如果文件名包含_brain，那么title就是颅骨分离后的图像，否则就是原始图像
    if "_brain" in args.nii_path:
        title="预处理后的3D图像"
    else:
        title="原始3D图像"
    
    OrthoSlicer3D(img.dataobj, title=title).show()
    # OrthoSlicer3D(img3.dataobj,title=).show()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='nii show')
    parser.add_argument('--nii-path',default="ADNI_result/I131842_brain.nii.gz", type=str, help='nii file path')
    args = parser.parse_args()
    main(args)
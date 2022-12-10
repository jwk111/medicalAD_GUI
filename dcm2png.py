# 输入医院样本dcm文件夹，输出可以处理的nii文件
import dicom2nifti
import os
import nibabel as nib    #nii格式一般都会用到这个包
import imageio           #转换成图像

def dcm2nii(dcm_path, nii_path):
    # 读取路径中所有dicom文件，输出nii文件
    dicom2nifti.convert_directory(dcm_path, nii_path, compression=True, reorient=True)

#输入nii文件路径和之后输出的图片路径
def nii_to_image(filepath,savepath):

        #开始读取nii文件
    # img_path = os.path.join(filepath, filepath)
    img = nib.load(filepath)                #读取nii
    img_fdata = img.get_fdata()
    # fname = savepath.replace('.nii.gz','')            #去掉nii的后缀名
    l = 1       #每次取的图片大小
    #开始转换为图像
    (x,y,z) = img.shape         #z/2=91
                               #一个nii出来25个图，所以要有k个nii，用来作为之后的名字叠加参数
    for i in range(z):                      #z是图像的序列
        if i==z/2:       #选择z序列中间90序号前10张图和后15张图
            silce = img_fdata[:,:,i]          #选择哪个方向的切片都可以,第三个维度是对的
            # print('{}.png'.format(2*j))
            imageio.imwrite(savepath+".png", silce)  

def preprocess(dcmPath, niiDir):
    if not os.path.exists(niiDir):
        os.makedirs(niiDir)

    # 判断nii路径是否存在，不存在则创建
    if not os.path.exists(niiDir):
        os.makedirs(niiDir)
    dcmName = os.path.split(dcmPath)[1]
    dcm2nii(dcmPath, niiDir)
    rawDir = niiDir + "/" + dcmName
    rawPath = niiDir + "/" + dcmName + ".nii.gz"
    # 使用FSL对图像进行颅骨剥离
    print("FSL start......\n")
    # 图像坐在的目录
    #------------------------图像路径需更改------------------------#
    #MNI模板文件路径
    ref = "/media/z840/HDD_6T/Linux_DATA/jwk/medical/FSL/fsl/data/standard/MNI152lin_T1_1mm.nii.gz"

    #------------------------输出路径需更改------------------------#
    #子文件要包含文件夹flirt和brain
    #进入生数据目录才能进行flirt和bet,";"是命令的间隔符，介于两个命令之间，可以用“&&”代替
    file = rawPath
    # 将文件路径和文件名分离
    print("absolut file:",file)
    filename0 = os.path.split(file)[1] # 将路径名和文件名分开
    filename1 = filename0.split(".n")[0] # 取文件名 
    filename2 = file.split(".n")[0]#包含路径和文件名，无扩展名
    flirt_out = filename2 + "_flirt.nii.gz"
    bet_out = filename2 + "_brain.nii.gz"
    #线性配准命令
    flirt_cmd = "flirt "+"-in "+file+" -ref "+ref+" -out "+ flirt_out
    #颅骨分割命令
    bet_cmd = "bet "+ flirt_out +" "+ bet_out +" -R"
    os.system(flirt_cmd)
    os.system(bet_cmd)
    #bet命令运行一定要注意当前运行路径！！！！！不然无法运行
    nii_to_image(bet_out,rawDir)

def main():
    #------------------------图像路径需更改------------------------#
    # dicom文件夹路径
    dcmPath = "/media/z840/HDD_6T/Linux_DATA/jwk/medical/AD/ADNI_dcm"
    niiDir = "ADNI_result"
    preprocess(dcmPath, niiDir)

if __name__ == '__main__':
    main()
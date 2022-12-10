import streamlit as st
import os
import tkinter as tk
from tkinter import filedialog
import time
from PIL import Image
import dicom2nifti
import time
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg("/media/z840/HDD_6T/Linux_DATA/jwk/medical/second_EI/ConvNeXt/background.png")
time.sleep(1)
st.title("医疗大数据识别平台")

# root  = tk.Tk()
# root.withdraw()
# root.wm_attributes('-topmost',1)
# clicked = st.button("选择数据文件夹")
# if clicked:
#     folder_path = st.text_input("selected folder:",filedialog.askdirectory(master=root))

# uploadfiles = st.file_uploader("upload file",accept_multiple_files=True)
# for file in uploadfiles:
#     if file.size > 0:
#         st.write(file.name)
# if uploadfiles.count > 0:
#     dicom2nifti.dicom_series_to_nifti(uploadfiles, "/media/z840/HDD_1/LINUX/jwk/医学图像项目/数据预处理/reprogressGUI/output.nii", reorient_nifti=True)

# 输入文件夹路径
sub1 = st.subheader("dicom文件夹路径")
folder_path = st.text_input("dicom文件夹路径","/media/z840/HDD_6T/Linux_DATA/jwk/medical/AD/I131842",label_visibility="collapsed")
# 输入保存文件夹路径
sub2 = st.subheader("保存结果路径")
save_folder_path = st.text_input("保存结果路径","/media/z840/HDD_6T/Linux_DATA/jwk/medical/second_EI/ConvNeXt/ADNI_result",label_visibility="collapsed")


if folder_path:
    pycmd = "python /media/z840/HDD_6T/Linux_DATA/jwk/medical/second_EI/ConvNeXt/predict_final.py --dcm-path {} --save-path {}".format(folder_path,save_folder_path)
    # gncmd = "gnome-terminal -e 'bash -c \"{}; exec bash\"'".format(pycmd)
    gncmd = "gnome-terminal -e 'bash -c \"{};\"'".format(pycmd)

# 开始识别
# 三个按钮在一行
col1, col2, col3 = st.columns(3)
with col1:
    recogButton = st.button("开始识别")
with col2:
    origShowButton = st.button("显示原始3D图像")
with col3:
    brainShowButton = st.button("显示处理后3D图像")

if recogButton:
    # recogButton.disabled = True
    image_path = save_folder_path + "/result.png"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption='预测结果')
    else:
        start = time.time()

        st.info("识别中...")
        os.system(pycmd)
        while(1):
            if os.path.exists(image_path):
                time.sleep(1)
                image = Image.open(image_path)
                st.image(image, caption='预测结果')
                end = time.time()
                st.success("识别完成，耗时{:.3}s".format(end-start))
                break
            else:
                st.error("输入正确的文件夹路径")
                break
    # recogButton.disabled = False

if origShowButton:
    origImage = folder_path.split("/")[-1]
    origPath = save_folder_path + "/" +origImage + ".nii.gz"
    if os.path.exists(origPath):
        time.sleep(1)
        niipy = "python /media/z840/HDD_6T/Linux_DATA/jwk/medical/second_EI/ConvNeXt/nii_show.py --nii-path {}".format(origPath)
        niicmd = "gnome-terminal -e 'bash -c \"{};\"'".format(niipy)
        os.system(niicmd)
    else:
        st.warning("请先识别")

if brainShowButton:
    brainImage = folder_path.split("/")[-1]
    brainPath = save_folder_path + "/" + brainImage + "_brain.nii.gz"
    if os.path.exists(brainPath):
        time.sleep(1)
        niipy = "python /media/z840/HDD_6T/Linux_DATA/jwk/medical/second_EI/ConvNeXt/nii_show.py --nii-path {}".format(brainPath)
        niicmd = "gnome-terminal -e 'bash -c \"{};\"'".format(niipy)
        os.system(niicmd)
    else:
        st.warning("请先识别")




    
    

import argparse
import os
import json
import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

from model import convnext_tiny_coor as create_model
from dcm2png import dcm2nii,preprocess,nii_to_image


def main(args):
    # 数据转化阶段，dicom转换为png
    preprocess(args.dcm_path, args.save_path)
    # 显示nii文件
    plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"using {device} device.")
    
    num_classes = 3
    img_size = 224
    data_transform = transforms.Compose(
        [transforms.Resize(int(img_size * 1.14)),
         transforms.CenterCrop(img_size),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # load image
    dcmName = os.path.split(args.dcm_path)[1]
    img_path = args.save_path + "/" + dcmName + ".png"
    assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
    img = Image.open(img_path)
    # img转为3通道
    if img.mode != "RGB":
        img = img.convert("RGB")
    # plt.imshow调整高度
    plt.figure(figsize=(6,5.5))
    plt.imshow(img)
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    json_file = open(json_path, "r")
    class_indict = json.load(json_file)

    # create model
    model = create_model(num_classes=num_classes).to(device)
    # load model weights
    model_weight_path = "runs/coor+convnext_bach16_9606/best_model.pth"
    model.load_state_dict(torch.load(model_weight_path, map_location=device))
    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()

    # print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_cla)],
    #                                              predict[predict_cla].numpy())
    # 新建字符数组，大小为3
    print_res = [0,0,0]
    # 阿尔茨海默症类别数组
    adClass = ["阿尔茨海默症(AD)","轻型认知障碍(MCI)","正常认知(NC)"]
    for i in range(len(predict)):
        print_res[i] = "类别: {}   概率: {:.3%}".format(adClass[i],
                                                    predict[i].numpy())
    plt.title(print_res[0]+"\n"+print_res[1]+"\n"+print_res[2])
    # plt.title(print_res)
    for i in range(len(predict)):
        print("类别: {:10}   概率: {:.3%}".format(class_indict[str(i)],
                                                  predict[i].numpy()))
    # plt.show()
    plt.savefig(args.save_path + "/" + "result" + ".png")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict Image')
    parser.add_argument("--dcm-path",default="/media/z840/HDD_6T/Linux_DATA/jwk/medical/AD/13888165/1.2.840.113619.2.388.57473.11731677.12945.1626570520.720", type=str, help='input dicom path')
    parser.add_argument("--save-path",default="/media/z840/HDD_6T/Linux_DATA/jwk/medical/second_EI/ConvNeXt/NII", type=str, help='save image path')
    opt = parser.parse_args()
    main(opt)


# python predict_final.py --dcm-path /media/z840/HDD_1/LINUX/jwk/医学图像项目/数据预处理/reprogressGUI/AD/13888165/1.2.840.113619.2.388.57473.11731677.12945.1626570520.720 --save-path /media/z840/HDD_1/LINUX/jwk/second_EI/ConvNeXt/result
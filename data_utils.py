from torchvision import datasets,transforms
import os
from skimage import  io
import torchvision.datasets.mnist as mnist
from PIL import Image
from torch.utils.data import Dataset,DataLoader

def get_public_dataset(args):
    if args.dataset =='mnist':
        data_dir ='Data/mnist/'
    apply_transform = transforms.Compose([transforms.ToTensor(),
                                          transforms.Normalize((0.1307,), (0.3081,))])
    data_train = datasets.MNIST(root=data_dir,train=True,download=False,transform=apply_transform)
    data_test = datasets.MNIST(root=data_dir,train=False,download=False,transform=apply_transform)
    return data_train,data_test

def convert_to_img(root,train_set,test_set,train=True):
    if (train):
        f = open(root + 'train.txt', 'w')
        data_path = root + '/train/'
        if (not os.path.exists(data_path)):
            os.makedirs(data_path)
        for i, (img, label) in enumerate(zip(train_set[0], train_set[1])):
            img_path = data_path + str(i) + '.jpg'
            io.imsave(img_path, img.numpy())
            f.write(img_path + ' ' + str(label.item()) + '\n')
        f.close()
    else:
        f = open(root + 'test.txt', 'w')
        data_path = root + '/test/'
        if (not os.path.exists(data_path)):
            os.makedirs(data_path)
        for i, (img, label) in enumerate(zip(test_set[0], test_set[1])):
            img_path = data_path + str(i) + '.jpg'
            io.imsave(img_path, img.numpy())
            f.write(img_path + ' ' + str(label.item()) + '\n')
        f.close()

def init_private_dataset(args):
    if args.private_dataset == 'FEMNIST':
        rootraw = "Data/FEMNIST/raw/"
        root = "Data/FEMNIST/"
    train_set = (
        mnist.read_image_file(os.path.join(rootraw, 'emnist-letters-train-images-idx3-ubyte')),
        mnist.read_label_file(os.path.join(rootraw, 'emnist-letters-train-labels-idx1-ubyte'))
    )

    test_set = (
        mnist.read_image_file(os.path.join(rootraw, 'emnist-letters-test-images-idx3-ubyte')),
        mnist.read_label_file(os.path.join(rootraw, 'emnist-letters-test-labels-idx1-ubyte'))
    )

    print("train set:", train_set[0].size())
    print("test set:", test_set[0].size())

    convert_to_img(root,train_set,test_set,train=True)
    convert_to_img(root,train_set,test_set,train=False)


def default_loader(path):
    return Image.open(path)

# 用于获得未处理过的私有数据集
def get_private_dataset(args):
    if args.private_dataset == 'FEMNIST':
        root = "Data/FEMNIST/"
    class MyDataset(Dataset):
        # 当我们对类的属性item进行下标的操作时，首先会被__getitem__()、__setitem__()、__delitem__()拦截，从而执行我们在方法中设定的操作，如赋值，修改内容，删除内容等等。
        def __init__(self, txt, transform=None, target_transform=None, loader=default_loader):
            fh = open(txt, 'r')
            imgs = []
            for line in fh:
                line = line.strip('\n')
                line = line.rstrip()
                words = line.split()
                imgs.append((words[0], int(words[1]))) # 在这里对数据进行修改
            self.imgs = imgs
            self.transform = transform
            self.target_transform = target_transform
            self.loader = loader

        def __getitem__(self, index):
            fn, label = self.imgs[index]
            img = self.loader(fn)
            if self.transform is not None:
                img = self.transform(img)
            return img, label

        def __len__(self):
            return len(self.imgs)
    apply_transform = transforms.Compose([transforms.ToTensor(),
                                          transforms.Normalize((0.1307,), (0.3081,))])
    data_train = MyDataset(txt=root + 'train.txt', transform=apply_transform)
    data_test = MyDataset(txt=root + 'test.txt', transform=apply_transform)
    return  data_train,data_test

# 用于获得处理过的数据集限制了标签的值
def get_private_dataset_balanced(args):
    if args.private_dataset == 'FEMNIST':
        root = "Data/FEMNIST/"
    private_data_index = [10,11,12,13,14,15]
    class MyDataset(Dataset):
        # 当我们对类的属性item进行下标的操作时，首先会被__getitem__()、__setitem__()、__delitem__()拦截，从而执行我们在方法中设定的操作，如赋值，修改内容，删除内容等等。
        def __init__(self, txt, transform=None, target_transform=None, loader=default_loader):
            fh = open(txt, 'r')
            # i = 0
            imgs = []
            for line in fh:
                line = line.strip('\n')
                line = line.rstrip()
                words = line.split()
                if (int(words[1])+9) in private_data_index:
                    # i = i+1
                    imgs.append((words[0], (int(words[1])+9))) # 在这里对数据进行修改
            # print(i)
            self.imgs = imgs
            self.transform = transform
            self.target_transform = target_transform
            self.loader = loader

        def __getitem__(self, index):
            fn, label = self.imgs[index]
            img = self.loader(fn)
            if self.transform is not None:
                img = self.transform(img)
            return img, label

        def __len__(self):
            return len(self.imgs)

    apply_transform = transforms.Compose([transforms.ToTensor(),
                                          transforms.Normalize((0.1307,), (0.3081,))])
    data_train = MyDataset(txt=root + 'train.txt', transform=apply_transform)
    data_test = MyDataset(txt=root + 'test.txt', transform=apply_transform)
    return  data_train,data_test

import  numpy as np
import os
from option import args_parser


dict = {14: [0, 2, 14, 22, 23, 24, 28, 31, 35, 58, 63, 64, 72, 77, 87, 90, 91, 94, 95, 97, 104, 112, 138, 144, 153, 165, 179, 191, 195, 198, 207, 208, 214, 219, 221, 226, 248, 254, 255, 259, 261, 262, 264, 283, 285, 286, 295, 298, 299, 306, 310, 317, 324, 329, 337, 343, 351, 357, 366, 370, 371, 376, 380, 393, 394, 395, 404, 405, 408, 419, 433, 437, 439, 448, 450, 456, 461, 480, 481, 490, 499, 503, 507, 508, 512, 522, 527, 531, 540, 541, 555, 558, 563, 564, 570, 573, 582, 584, 591, 594, 599, 603, 607, 609, 610, 612, 621, 627, 628, 634, 650, 652, 667, 668, 696, 702, 710, 714, 715, 717, 726, 728, 729, 730, 739, 743, 748, 750, 762, 769, 775, 782, 783, 792, 798, 808, 811, 817, 823, 826, 834, 851, 854, 857, 858, 860, 864, 867, 868, 870, 876, 879, 881, 884, 898, 900, 919, 934, 938, 941, 949, 950, 954, 956, 958, 972, 986, 990, 1019, 1020, 1022, 1027, 1029, 1031, 1032, 1036, 1038, 1039, 1040, 1051, 1055, 1077, 1079, 1087, 1094, 1106, 1110, 1119, 1128, 1130, 1141, 1145, 1154, 1161, 1166, 1181, 1186, 1194, 1206, 1208, 1220, 1221, 1223, 1228, 1243, 1247, 1251, 1273, 1295, 1299, 1301, 1308, 1331, 1340, 1342, 1371, 1375, 1378, 1379, 1381, 1388, 1395, 1398, 1400, 1402, 1405, 1406, 1407, 1417, 1422, 1427, 1430, 1436, 1452, 1454, 1464, 1471, 1472, 1478, 1479, 1484, 1493, 1494, 1499, 1504, 1508, 1522, 1523, 1525, 1541, 1546, 1547, 1550, 1551, 1553, 1556, 1558, 1565, 1566, 1573, 1574, 1578, 1583, 1584, 1596, 1598, 1605, 1608, 1612, 1617, 1621, 1623, 1642, 1645, 1646, 1654, 1681, 1683, 1687, 1688, 1689, 1704, 1714, 1716, 1718, 1724, 1725, 1731, 1732, 1733, 1735, 1736, 1740, 1745, 1771, 1772, 1785, 1798, 1799, 1804, 1805, 1807, 1810, 1813, 1817, 1818, 1843, 1846, 1848, 1863, 1864, 1884, 1890, 1899, 1902, 1904, 1906, 1914, 1920, 1923, 1925, 1945, 1952, 1957, 1959, 1960, 1968, 1974, 1975, 2001, 2004, 2011, 2016, 2041, 2042, 2057, 2060, 2071, 2075, 2077, 2081, 2094, 2100, 2102, 2104, 2115, 2117, 2118, 2119, 2149, 2151, 2153, 2154, 2155, 2161, 2162, 2166, 2172, 2188, 2191, 2198, 2202, 2212, 2219, 2223, 2236, 2237, 2243, 2244, 2254, 2255, 2258, 2263, 2274, 2278, 2282, 2283, 2286, 2295, 2300, 2305, 2325, 2329, 2333, 2336, 2351, 2353, 2358, 2360, 2363, 2366, 2377, 2382, 2390, 2391, 2394, 2401, 2423, 2435, 2437, 2444, 2450, 2453, 2457, 2458, 2461, 2464, 2465, 2467, 2475, 2483, 2502, 2504, 2513, 2524, 2526, 2527, 2529, 2532, 2543, 2547, 2551, 2557, 2570, 2573, 2587, 2590, 2593, 2602, 2609, 2612, 2628, 2641, 2644, 2662, 2666, 2673, 2674, 2677, 2696, 2697, 2698, 2699, 2704, 2705, 2725, 2728, 2729, 2737, 2745, 2746, 2747, 2751, 2752, 2753, 2756, 2765, 2774, 2776, 2778, 2779, 2780, 2784, 2791, 2806, 2810, 2813, 2814, 2822, 2825, 2826, 2831, 2836, 2839, 2845, 2850, 2852, 2853, 2855, 2860, 2865, 2878, 2879, 2884, 2885, 2888, 2893, 2898, 2902, 2903, 2906, 2910, 2930, 2937, 2940, 2948, 2952, 2959, 2964, 2966, 2972, 2980, 2983, 2986, 2994, 2997, 3003, 3005, 3010, 3019, 3022, 3026, 3028, 3030, 3034, 3035, 3061, 3062, 3066, 3087, 3102, 3108, 3121, 3122, 3124, 3130, 3133, 3134, 3141, 3146, 3150, 3152, 3162, 3165, 3174, 3177, 3183, 3197, 3198, 3205, 3215, 3218, 3219, 3232, 3235, 3236, 3240, 3259, 3262, 3276, 3277, 3279, 3282, 3283, 3289, 3306, 3307, 3311, 3316, 3324, 3333, 3347, 3350, 3358, 3359, 3368, 3374, 3390, 3394, 3400, 3408, 3436, 3441, 3442, 3459, 3461, 3469, 3478, 3484, 3492, 3497, 3513, 3521, 3522, 3524, 3531, 3536, 3540, 3543, 3544, 3547, 3550, 3551, 3561, 3570, 3573, 3578, 3581, 3582, 3584, 3585, 3589, 3591, 3594, 3609, 3613, 3614, 3619, 3628, 3633, 3634, 3637, 3638, 3642, 3650, 3653, 3655, 3656, 3658, 3660, 3661, 3663, 3666, 3669, 3677, 3688, 3695, 3705, 3719, 3724, 3725, 3726, 3736, 3742, 3747, 3753, 3759, 3763, 3774, 3775, 3778, 3787, 3799, 3805, 3817, 3823, 3837, 3840, 3841, 3842, 3844, 3853, 3864, 3865, 3874, 3878, 3881, 3885, 3900, 3904, 3920, 3926, 3928, 3934, 3937, 3957, 3964, 3966, 3975, 3976, 3987, 3991, 3999, 4021, 4022, 4031, 4044, 4047, 4056, 4063, 4068, 4070, 4079, 4088, 4089, 4106, 4107, 4124, 4125, 4129, 4140, 4147, 4148, 4150, 4153, 4155, 4169, 4173, 4174, 4176, 4178, 4189, 4190, 4195, 4198, 4202, 4218, 4225, 4226, 4232, 4240, 4244, 4257, 4278, 4281, 4288, 4291, 4300, 4301, 4305, 4307, 4324, 4326, 4334, 4335, 4337, 4347, 4348, 4357, 4358, 4359, 4362, 4368, 4371, 4387, 4389, 4393, 4394, 4411, 4418, 4422, 4434, 4439, 4447, 4456, 4457, 4473, 4486, 4493, 4494, 4496, 4497, 4502, 4504, 4507, 4513, 4514, 4518, 4524, 4536, 4542, 4548, 4557, 4569, 4576, 4578, 4584, 4586, 4596, 4601, 4616, 4628, 4631, 4645, 4647, 4659, 4665, 4670, 4673, 4679, 4681, 4682, 4683, 4685, 4696, 4699, 4711, 4713, 4715, 4743, 4761, 4781, 4785, 4790, 4791, 4797, 4803, 4804, 4817, 4819, 4823, 4824, 4832, 4836, 4839, 4840, 4850, 4851, 4865, 4871, 4877, 4882, 4883, 4888, 4890, 4893, 4895, 4896, 4898, 4904, 4911, 4923, 4925, 4929, 4930, 4933, 4939, 4943, 4945, 4946, 4950, 4951, 4953, 4957, 4965, 4966, 4970, 4977, 4979, 4986, 4987, 4988, 4997, 5015, 5016, 5022, 5024, 5026, 5037, 5041, 5043, 5045, 5050, 5059, 5063, 5066, 5084, 5090, 5092, 5107, 5110, 5122, 5138, 5139, 5140, 5149, 5156, 5165, 5168, 5178, 5197, 5201, 5204, 5205, 5206, 5211, 5225, 5229, 5231, 5237, 5250, 5252, 5253, 5258, 5270, 5277, 5278, 5283, 5288, 5301, 5304, 5306, 5315, 5326, 5327, 5329, 5330, 5347, 5379, 5389, 5392, 5409, 5414, 5417, 5424],
        11: [1, 9, 16, 17, 19, 21, 27, 40, 41, 42, 47, 52, 53, 66, 78, 80, 86, 107, 115, 118, 120, 121, 129, 131, 133, 148, 149, 150, 156, 159, 162, 166, 167, 168, 193, 206, 213, 215, 223, 225, 230, 240, 257, 258, 263, 265, 267, 270, 271, 278, 281, 289, 320, 322, 325, 326, 332, 334, 341, 345, 346, 352, 360, 363, 365, 369, 372, 382, 383, 390, 410, 415, 418, 426, 430, 431, 435, 454, 462, 476, 486, 489, 493, 496, 506, 513, 518, 525, 526, 533, 557, 571, 593, 597, 615, 625, 629, 633, 637, 657, 670, 671, 672, 673, 681, 684, 692, 695, 700, 706, 716, 719, 724, 734, 735, 755, 756, 759, 763, 771, 773, 784, 786, 789, 794, 806, 820, 822, 840, 849, 852, 853, 866, 875, 894, 918, 920, 923, 927, 937, 943, 944, 960, 965, 966, 967, 973, 980, 984, 991, 1012, 1014, 1015, 1017, 1018, 1049, 1056, 1061, 1065, 1066, 1069, 1074, 1075, 1083, 1098, 1101, 1102, 1107, 1112, 1123, 1134, 1137, 1139, 1140, 1143, 1144, 1149, 1171, 1173, 1178, 1179, 1183, 1187, 1188, 1193, 1207, 1210, 1215, 1222, 1226, 1230, 1237, 1239, 1240, 1248, 1255, 1258, 1261, 1263, 1266, 1268, 1276, 1278, 1286, 1288, 1302, 1307, 1311, 1313, 1316, 1320, 1321, 1325, 1326, 1328, 1334, 1367, 1370, 1373, 1377, 1383, 1391, 1392, 1394, 1418, 1423, 1433, 1437, 1449, 1458, 1462, 1467, 1469, 1473, 1474, 1488, 1500, 1505, 1506, 1511, 1518, 1528, 1529, 1533, 1536, 1537, 1539, 1549, 1561, 1567, 1572, 1582, 1591, 1607, 1629, 1631, 1632, 1635, 1637, 1647, 1649, 1661, 1668, 1669, 1672, 1684, 1685, 1686, 1696, 1713, 1720, 1729, 1749, 1752, 1767, 1768, 1774, 1775, 1779, 1788, 1806, 1809, 1812, 1824, 1828, 1850, 1865, 1867, 1871, 1876, 1881, 1883, 1885, 1887, 1888, 1889, 1900, 1901, 1908, 1922, 1928, 1938, 1942, 1944, 1954, 1958, 1964, 1973, 1978, 1983, 1984, 1985, 1989, 2020, 2022, 2024, 2039, 2047, 2049, 2054, 2055, 2063, 2065, 2070, 2080, 2087, 2091, 2113, 2116, 2135, 2136, 2140, 2142, 2145, 2146, 2148, 2164, 2170, 2192, 2193, 2194, 2204, 2207, 2210, 2224, 2227, 2232, 2238, 2239, 2257, 2264, 2265, 2267, 2268, 2277, 2287, 2292, 2322, 2324, 2327, 2340, 2341, 2345, 2367, 2403, 2412, 2418, 2420, 2432, 2436, 2438, 2448, 2449, 2455, 2469, 2476, 2477, 2491, 2505, 2506, 2509, 2523, 2531, 2537, 2538, 2545, 2559, 2560, 2562, 2564, 2576, 2578, 2580, 2598, 2603, 2608, 2619, 2620, 2623, 2624, 2639, 2642, 2643, 2649, 2651, 2671, 2682, 2683, 2684, 2686, 2687, 2695, 2709, 2717, 2719, 2731, 2734, 2748, 2762, 2763, 2773, 2783, 2794, 2798, 2800, 2812, 2816, 2817, 2841, 2847, 2856, 2862, 2864, 2870, 2871, 2874, 2880, 2881, 2890, 2891, 2892, 2896, 2905, 2913, 2914, 2917, 2935, 2936, 2938, 2939, 2947, 2949, 2951, 2954, 2956, 2958, 2962, 2965, 2967, 2968, 2993, 2999, 3000, 3004, 3007, 3009, 3011, 3015, 3025, 3037, 3042, 3054, 3055, 3063, 3074, 3079, 3092, 3097, 3105, 3111, 3112, 3113, 3116, 3128, 3129, 3131, 3132, 3153, 3155, 3156, 3170, 3181, 3182, 3188, 3189, 3194, 3212, 3213, 3217, 3222, 3229, 3233, 3238, 3251, 3253, 3290, 3293, 3294, 3297, 3309, 3331, 3338, 3341, 3342, 3346, 3364, 3369, 3382, 3383, 3384, 3399, 3402, 3412, 3413, 3415, 3420, 3437, 3443, 3444, 3445, 3446, 3448, 3451, 3462, 3464, 3470, 3472, 3479, 3480, 3481, 3482, 3483, 3486, 3490, 3496, 3498, 3506, 3507, 3523, 3539, 3546, 3548, 3549, 3574, 3580, 3590, 3596, 3601, 3610, 3615, 3626, 3632, 3639, 3657, 3662, 3664, 3667, 3670, 3686, 3687, 3691, 3696, 3698, 3706, 3707, 3710, 3711, 3714, 3729, 3737, 3745, 3756, 3760, 3762, 3765, 3766, 3768, 3773, 3776, 3786, 3790, 3794, 3796, 3797, 3811, 3813, 3816, 3824, 3838, 3843, 3867, 3870, 3872, 3875, 3886, 3888, 3893, 3895, 3906, 3911, 3921, 3922, 3938, 3949, 3950, 3955, 3960, 3970, 3971, 3982, 3984, 3988, 3997, 3998, 4009, 4012, 4014, 4016, 4029, 4033, 4035, 4039, 4041, 4048, 4051, 4065, 4073, 4080, 4085, 4103, 4109, 4128, 4131, 4137, 4138, 4142, 4146, 4159, 4165, 4171, 4172, 4175, 4179, 4182, 4197, 4199, 4201, 4207, 4209, 4212, 4215, 4236, 4245, 4253, 4255, 4256, 4258, 4266, 4269, 4275, 4282, 4286, 4289, 4294, 4296, 4297, 4302, 4311, 4312, 4313, 4316, 4322, 4325, 4333, 4342, 4349, 4351, 4352, 4354, 4355, 4370, 4372, 4373, 4376, 4386, 4399, 4401, 4405, 4406, 4412, 4413, 4421, 4428, 4437, 4449, 4463, 4485, 4509, 4511, 4519, 4522, 4525, 4526, 4530, 4538, 4541, 4543, 4545, 4547, 4551, 4553, 4555, 4559, 4565, 4566, 4572, 4575, 4579, 4580, 4581, 4587, 4590, 4602, 4606, 4610, 4611, 4615, 4621, 4622, 4630, 4640, 4642, 4644, 4651, 4660, 4666, 4667, 4672, 4674, 4677, 4688, 4694, 4700, 4701, 4706, 4707, 4721, 4723, 4728, 4734, 4741, 4744, 4757, 4758, 4759, 4760, 4763, 4776, 4779, 4793, 4805, 4806, 4811, 4812, 4814, 4816, 4826, 4827, 4838, 4844, 4845, 4857, 4859, 4864, 4872, 4901, 4903, 4907, 4913, 4916, 4919, 4920, 4921, 4927, 4944, 4956, 4967, 4971, 4973, 4981, 4994, 5001, 5003, 5011, 5014, 5017, 5020, 5032, 5047, 5074, 5076, 5102, 5104, 5114, 5117, 5118, 5120, 5126, 5128, 5131, 5133, 5137, 5145, 5148, 5150, 5151, 5158, 5167, 5170, 5171, 5174, 5179, 5180, 5181, 5191, 5192, 5200, 5203, 5208, 5209, 5215, 5217, 5218, 5219, 5220, 5221, 5243, 5244, 5246, 5255, 5257, 5261, 5271, 5275, 5289, 5291, 5292, 5308, 5311, 5312, 5328, 5338, 5340, 5341, 5346, 5354, 5355, 5356, 5357, 5358, 5369, 5370, 5371, 5374, 5376, 5387, 5398, 5405, 5408, 5410, 5412, 5418],
        10: [3, 4, 5, 7, 13, 18, 20, 55, 59, 67, 74, 82, 88, 96, 106, 110, 114, 116, 119, 128, 132, 137, 139, 146, 154, 158, 160, 173, 176, 180, 196, 203, 209, 220, 229, 232, 234, 241, 249, 252, 253, 256, 268, 279, 280, 282, 290, 293, 294, 296, 297, 300, 301, 307, 327, 339, 342, 354, 364, 384, 387, 388, 403, 406, 407, 414, 420, 421, 422, 424, 429, 444, 452, 453, 469, 470, 477, 483, 484, 488, 498, 510, 514, 517, 519, 530, 532, 534, 538, 543, 544, 547, 552, 559, 565, 576, 583, 585, 586, 592, 596, 598, 600, 620, 640, 644, 646, 647, 649, 653, 658, 663, 669, 674, 683, 687, 690, 691, 693, 697, 712, 722, 727, 732, 737, 740, 741, 742, 752, 757, 770, 776, 779, 781, 787, 793, 797, 809, 810, 813, 815, 830, 832, 843, 850, 869, 872, 873, 874, 882, 892, 893, 903, 907, 910, 914, 915, 925, 932, 942, 952, 953, 959, 963, 969, 971, 976, 977, 978, 982, 988, 989, 994, 1000, 1001, 1006, 1021, 1023, 1024, 1025, 1028, 1044, 1047, 1052, 1057, 1058, 1064, 1068, 1073, 1092, 1093, 1095, 1104, 1109, 1113, 1122, 1125, 1133, 1135, 1152, 1160, 1162, 1163, 1164, 1167, 1170, 1172, 1184, 1198, 1200, 1202, 1203, 1212, 1219, 1225, 1246, 1250, 1256, 1269, 1282, 1291, 1296, 1297, 1303, 1309, 1310, 1314, 1315, 1317, 1318, 1322, 1338, 1343, 1344, 1346, 1349, 1364, 1365, 1380, 1385, 1386, 1401, 1411, 1415, 1419, 1421, 1426, 1445, 1447, 1450, 1456, 1457, 1460, 1475, 1477, 1480, 1481, 1483, 1489, 1491, 1497, 1498, 1502, 1509, 1520, 1524, 1526, 1543, 1548, 1575, 1579, 1588, 1592, 1597, 1603, 1614, 1619, 1620, 1624, 1639, 1644, 1650, 1651, 1652, 1653, 1655, 1656, 1663, 1676, 1717, 1726, 1728, 1744, 1758, 1760, 1764, 1766, 1769, 1777, 1780, 1783, 1787, 1789, 1790, 1803, 1811, 1814, 1820, 1823, 1827, 1830, 1834, 1837, 1838, 1841, 1849, 1854, 1855, 1861, 1872, 1879, 1880, 1886, 1897, 1905, 1913, 1917, 1918, 1937, 1947, 1948, 1953, 1956, 1967, 1977, 1988, 1991, 1992, 1996, 1999, 2002, 2009, 2010, 2014, 2015, 2017, 2018, 2021, 2025, 2033, 2043, 2050, 2053, 2058, 2062, 2066, 2068, 2076, 2085, 2090, 2093, 2095, 2103, 2105, 2112, 2114, 2120, 2122, 2125, 2129, 2130, 2131, 2133, 2134, 2147, 2152, 2157, 2167, 2174, 2175, 2182, 2186, 2195, 2201, 2214, 2220, 2222, 2228, 2229, 2230, 2262, 2273, 2275, 2276, 2279, 2288, 2289, 2293, 2297, 2301, 2314, 2328, 2330, 2332, 2338, 2339, 2347, 2356, 2357, 2359, 2372, 2374, 2376, 2379, 2385, 2386, 2392, 2395, 2396, 2407, 2411, 2413, 2439, 2440, 2441, 2442, 2443, 2452, 2474, 2479, 2481, 2488, 2496, 2497, 2498, 2499, 2500, 2522, 2525, 2528, 2530, 2536, 2541, 2542, 2544, 2549, 2553, 2561, 2567, 2569, 2575, 2579, 2581, 2583, 2585, 2586, 2592, 2605, 2610, 2625, 2627, 2632, 2633, 2635, 2640, 2645, 2650, 2654, 2656, 2665, 2676, 2678, 2679, 2681, 2693, 2701, 2710, 2712, 2714, 2718, 2720, 2723, 2726, 2736, 2739, 2743, 2768, 2775, 2781, 2789, 2795, 2804, 2830, 2833, 2840, 2851, 2854, 2859, 2863, 2867, 2868, 2886, 2897, 2900, 2909, 2911, 2919, 2927, 2934, 2941, 2944, 2946, 2950, 2953, 2960, 2961, 2969, 2971, 2975, 2976, 2978, 2991, 2996, 2998, 3002, 3027, 3029, 3038, 3046, 3047, 3049, 3051, 3053, 3060, 3068, 3070, 3075, 3077, 3078, 3100, 3101, 3103, 3135, 3138, 3147, 3158, 3163, 3167, 3180, 3186, 3192, 3196, 3201, 3208, 3209, 3220, 3226, 3244, 3247, 3250, 3261, 3263, 3264, 3266, 3270, 3278, 3280, 3281, 3291, 3295, 3296, 3304, 3312, 3315, 3321, 3322, 3334, 3339, 3354, 3360, 3370, 3373, 3375, 3378, 3391, 3398, 3406, 3409, 3411, 3417, 3422, 3428, 3430, 3434, 3447, 3455, 3457, 3463, 3465, 3466, 3467, 3468, 3473, 3474, 3475, 3477, 3487, 3488, 3502, 3503, 3520, 3529, 3530, 3537, 3538, 3545, 3558, 3559, 3560, 3571, 3572, 3579, 3592, 3597, 3598, 3599, 3600, 3604, 3607, 3617, 3620, 3622, 3625, 3641, 3643, 3646, 3651, 3668, 3679, 3684, 3685, 3690, 3712, 3722, 3727, 3730, 3732, 3734, 3735, 3744, 3749, 3752, 3757, 3761, 3769, 3772, 3781, 3784, 3795, 3798, 3802, 3822, 3828, 3829, 3831, 3833, 3836, 3848, 3851, 3854, 3861, 3876, 3879, 3883, 3887, 3899, 3913, 3915, 3919, 3923, 3931, 3933, 3935, 3936, 3945, 3951, 3953, 3954, 3963, 3972, 3974, 3981, 3995, 3996, 4004, 4005, 4008, 4011, 4017, 4018, 4026, 4027, 4043, 4045, 4050, 4055, 4060, 4074, 4076, 4081, 4082, 4086, 4087, 4096, 4108, 4117, 4134, 4135, 4139, 4144, 4149, 4185, 4186, 4227, 4231, 4250, 4268, 4274, 4279, 4284, 4285, 4292, 4310, 4314, 4330, 4332, 4336, 4343, 4350, 4360, 4365, 4366, 4377, 4385, 4398, 4400, 4407, 4410, 4419, 4425, 4430, 4454, 4464, 4466, 4467, 4476, 4483, 4488, 4489, 4499, 4515, 4516, 4528, 4534, 4537, 4546, 4549, 4552, 4561, 4562, 4570, 4571, 4583, 4585, 4588, 4589, 4598, 4617, 4619, 4620, 4625, 4629, 4633, 4636, 4643, 4646, 4649, 4650, 4653, 4662, 4668, 4669, 4671, 4684, 4689, 4690, 4691, 4692, 4724, 4725, 4727, 4739, 4764, 4766, 4767, 4773, 4775, 4782, 4787, 4794, 4796, 4807, 4821, 4829, 4830, 4841, 4858, 4861, 4866, 4874, 4876, 4879, 4881, 4884, 4886, 4914, 4935, 4936, 4938, 4942, 4958, 4963, 4972, 4978, 4980, 4990, 4993, 4995, 5010, 5021, 5027, 5035, 5036, 5040, 5042, 5046, 5048, 5049, 5053, 5064, 5072, 5093, 5094, 5097, 5101, 5105, 5111, 5123, 5134, 5135, 5144, 5162, 5173, 5176, 5186, 5213, 5224, 5226, 5239, 5251, 5256, 5259, 5263, 5281, 5285, 5294, 5297, 5298, 5299, 5300, 5305, 5313, 5317, 5322, 5323, 5333, 5342, 5343, 5349, 5365, 5368, 5375, 5378, 5381, 5383, 5385, 5391, 5420, 5425],
        13: [6, 12, 29, 45, 49, 50, 51, 57, 60, 62, 69, 70, 81, 89, 98, 124, 125, 127, 130, 134, 140, 143, 157, 169, 178, 181, 183, 185, 187, 192, 194, 197, 200, 202, 204, 205, 217, 222, 238, 272, 277, 287, 288, 304, 309, 315, 316, 319, 323, 328, 330, 331, 333, 336, 347, 348, 350, 355, 359, 367, 373, 378, 385, 386, 397, 402, 412, 416, 436, 440, 441, 445, 449, 451, 458, 464, 466, 467, 468, 491, 492, 500, 505, 516, 521, 524, 528, 529, 537, 539, 542, 546, 553, 554, 566, 572, 574, 577, 578, 595, 602, 606, 616, 622, 635, 643, 651, 655, 659, 664, 677, 678, 679, 682, 694, 705, 709, 713, 720, 721, 725, 733, 738, 745, 753, 758, 761, 766, 767, 777, 790, 799, 803, 804, 819, 821, 825, 829, 839, 844, 859, 862, 865, 880, 887, 890, 891, 909, 911, 913, 916, 917, 921, 928, 930, 933, 935, 940, 946, 947, 957, 964, 968, 974, 979, 981, 983, 998, 1002, 1007, 1008, 1011, 1013, 1016, 1026, 1030, 1034, 1035, 1042, 1043, 1050, 1059, 1060, 1062, 1063, 1067, 1070, 1071, 1080, 1084, 1088, 1091, 1096, 1116, 1124, 1127, 1129, 1132, 1142, 1156, 1157, 1159, 1185, 1189, 1191, 1197, 1199, 1204, 1218, 1234, 1242, 1244, 1245, 1259, 1270, 1271, 1274, 1277, 1284, 1287, 1289, 1290, 1292, 1306, 1324, 1327, 1332, 1333, 1341, 1345, 1350, 1352, 1353, 1356, 1369, 1374, 1382, 1387, 1393, 1396, 1397, 1404, 1428, 1434, 1435, 1438, 1439, 1443, 1444, 1446, 1448, 1459, 1463, 1466, 1485, 1487, 1490, 1492, 1507, 1510, 1521, 1534, 1540, 1545, 1552, 1559, 1564, 1589, 1595, 1601, 1602, 1604, 1611, 1625, 1626, 1628, 1630, 1638, 1643, 1658, 1659, 1664, 1666, 1671, 1673, 1682, 1695, 1697, 1699, 1706, 1709, 1719, 1723, 1734, 1743, 1747, 1750, 1763, 1765, 1776, 1782, 1791, 1795, 1796, 1800, 1801, 1815, 1816, 1822, 1832, 1851, 1856, 1860, 1874, 1878, 1882, 1891, 1909, 1910, 1916, 1924, 1929, 1930, 1932, 1934, 1935, 1963, 1965, 1966, 1979, 1981, 1993, 1995, 2000, 2008, 2012, 2013, 2027, 2029, 2031, 2032, 2038, 2045, 2048, 2061, 2073, 2074, 2084, 2086, 2098, 2106, 2107, 2109, 2121, 2124, 2128, 2137, 2138, 2158, 2168, 2169, 2176, 2178, 2179, 2197, 2200, 2203, 2216, 2217, 2218, 2225, 2226, 2231, 2240, 2250, 2253, 2259, 2272, 2281, 2284, 2291, 2294, 2309, 2310, 2313, 2317, 2331, 2335, 2352, 2355, 2362, 2364, 2368, 2380, 2384, 2389, 2398, 2404, 2406, 2414, 2415, 2416, 2424, 2427, 2431, 2434, 2445, 2447, 2451, 2470, 2471, 2472, 2482, 2485, 2493, 2517, 2519, 2533, 2535, 2540, 2546, 2548, 2550, 2556, 2563, 2566, 2568, 2574, 2577, 2584, 2588, 2591, 2596, 2601, 2607, 2611, 2613, 2614, 2616, 2629, 2636, 2638, 2648, 2652, 2655, 2659, 2660, 2667, 2670, 2672, 2675, 2680, 2688, 2692, 2703, 2706, 2708, 2711, 2716, 2727, 2741, 2742, 2757, 2758, 2761, 2769, 2771, 2777, 2785, 2786, 2790, 2792, 2797, 2807, 2808, 2811, 2815, 2820, 2824, 2829, 2842, 2848, 2857, 2858, 2861, 2875, 2876, 2877, 2882, 2887, 2895, 2901, 2904, 2907, 2912, 2918, 2923, 2929, 2933, 2942, 2945, 2955, 2963, 2970, 2973, 2981, 2982, 2985, 2987, 2989, 2990, 3008, 3013, 3017, 3020, 3040, 3048, 3056, 3057, 3058, 3067, 3073, 3080, 3081, 3082, 3083, 3093, 3109, 3119, 3120, 3136, 3142, 3144, 3148, 3151, 3168, 3169, 3175, 3178, 3185, 3207, 3214, 3221, 3231, 3234, 3237, 3242, 3243, 3245, 3246, 3267, 3269, 3285, 3286, 3292, 3300, 3301, 3305, 3310, 3318, 3323, 3325, 3329, 3335, 3336, 3340, 3348, 3361, 3366, 3367, 3371, 3372, 3379, 3393, 3396, 3397, 3401, 3407, 3410, 3414, 3418, 3419, 3429, 3431, 3435, 3438, 3450, 3454, 3456, 3458, 3495, 3499, 3505, 3511, 3516, 3517, 3526, 3527, 3541, 3552, 3557, 3576, 3583, 3586, 3587, 3603, 3606, 3608, 3611, 3612, 3616, 3621, 3624, 3631, 3635, 3636, 3644, 3645, 3665, 3672, 3674, 3675, 3700, 3703, 3704, 3721, 3723, 3738, 3740, 3741, 3743, 3748, 3750, 3767, 3770, 3771, 3780, 3800, 3801, 3804, 3815, 3818, 3821, 3826, 3830, 3832, 3839, 3849, 3858, 3866, 3869, 3871, 3873, 3889, 3890, 3892, 3894, 3897, 3898, 3901, 3905, 3909, 3918, 3925, 3929, 3930, 3940, 3941, 3942, 3944, 3956, 3959, 3968, 3979, 3993, 3994, 4000, 4002, 4006, 4007, 4019, 4024, 4028, 4038, 4049, 4052, 4057, 4059, 4066, 4069, 4075, 4078, 4084, 4091, 4097, 4111, 4113, 4115, 4120, 4122, 4127, 4130, 4132, 4151, 4158, 4166, 4180, 4181, 4196, 4204, 4205, 4206, 4211, 4214, 4216, 4219, 4221, 4228, 4229, 4242, 4243, 4254, 4259, 4261, 4265, 4267, 4273, 4308, 4321, 4328, 4339, 4340, 4344, 4353, 4361, 4375, 4378, 4380, 4390, 4391, 4395, 4396, 4408, 4409, 4416, 4417, 4420, 4426, 4436, 4441, 4443, 4446, 4459, 4460, 4465, 4468, 4479, 4481, 4484, 4492, 4505, 4517, 4521, 4529, 4577, 4592, 4594, 4595, 4597, 4608, 4609, 4613, 4623, 4632, 4634, 4639, 4655, 4656, 4657, 4658, 4675, 4680, 4687, 4693, 4697, 4716, 4717, 4720, 4729, 4731, 4732, 4737, 4738, 4742, 4746, 4749, 4750, 4751, 4769, 4771, 4774, 4786, 4795, 4813, 4815, 4820, 4828, 4847, 4852, 4856, 4868, 4873, 4885, 4894, 4905, 4908, 4910, 4917, 4918, 4924, 4928, 4931, 4932, 4934, 4937, 4940, 4961, 4962, 4982, 4983, 4989, 4991, 4999, 5006, 5025, 5028, 5033, 5051, 5054, 5056, 5065, 5067, 5069, 5075, 5077, 5083, 5086, 5087, 5106, 5116, 5142, 5147, 5152, 5159, 5182, 5184, 5188, 5195, 5199, 5207, 5214, 5216, 5222, 5228, 5236, 5242, 5248, 5260, 5267, 5272, 5282, 5284, 5286, 5290, 5296, 5309, 5310, 5318, 5319, 5321, 5325, 5331, 5332, 5344, 5345, 5351, 5380, 5382, 5384, 5390, 5393, 5395, 5396, 5399, 5402, 5413, 5416, 5422],
        12: [8, 10, 25, 30, 33, 34, 36, 37, 38, 39, 46, 54, 56, 71, 75, 79, 83, 85, 92, 101, 103, 108, 111, 113, 117, 122, 135, 141, 142, 147, 152, 155, 170, 171, 174, 175, 177, 189, 190, 199, 201, 210, 211, 212, 216, 231, 236, 237, 242, 243, 244, 246, 250, 260, 266, 273, 274, 275, 276, 284, 292, 305, 308, 311, 312, 313, 335, 349, 353, 356, 361, 362, 368, 375, 377, 379, 392, 396, 398, 399, 400, 401, 417, 423, 425, 427, 428, 442, 447, 455, 460, 473, 474, 475, 482, 494, 497, 502, 509, 511, 515, 523, 549, 551, 556, 560, 561, 562, 568, 581, 590, 601, 605, 611, 613, 614, 617, 619, 623, 626, 630, 642, 645, 654, 656, 660, 662, 665, 666, 675, 680, 685, 686, 689, 699, 704, 711, 718, 723, 736, 749, 751, 754, 764, 772, 780, 788, 791, 795, 796, 800, 816, 818, 827, 828, 833, 835, 837, 838, 842, 845, 846, 847, 848, 856, 861, 863, 871, 877, 883, 885, 886, 888, 889, 895, 896, 901, 902, 904, 905, 906, 924, 929, 939, 948, 955, 961, 962, 985, 995, 996, 999, 1005, 1009, 1033, 1045, 1046, 1048, 1054, 1076, 1081, 1085, 1086, 1089, 1090, 1099, 1103, 1111, 1115, 1118, 1126, 1138, 1150, 1151, 1153, 1158, 1165, 1168, 1180, 1190, 1195, 1201, 1211, 1213, 1214, 1216, 1231, 1233, 1236, 1238, 1254, 1260, 1262, 1264, 1265, 1275, 1281, 1285, 1300, 1304, 1319, 1323, 1329, 1335, 1336, 1337, 1348, 1354, 1357, 1361, 1363, 1366, 1376, 1384, 1399, 1409, 1412, 1413, 1429, 1442, 1451, 1455, 1476, 1482, 1495, 1496, 1501, 1503, 1517, 1519, 1527, 1530, 1531, 1542, 1554, 1560, 1562, 1568, 1571, 1577, 1581, 1585, 1586, 1590, 1606, 1609, 1613, 1618, 1622, 1627, 1633, 1634, 1636, 1640, 1641, 1657, 1660, 1678, 1679, 1680, 1690, 1691, 1698, 1700, 1703, 1707, 1708, 1710, 1711, 1712, 1715, 1721, 1722, 1727, 1730, 1746, 1748, 1754, 1756, 1759, 1762, 1770, 1778, 1781, 1786, 1792, 1797, 1802, 1808, 1821, 1826, 1829, 1831, 1839, 1840, 1842, 1844, 1857, 1858, 1868, 1869, 1870, 1873, 1875, 1877, 1893, 1894, 1898, 1903, 1911, 1912, 1919, 1921, 1933, 1940, 1941, 1961, 1962, 1969, 1971, 1982, 1987, 1994, 1997, 1998, 2005, 2006, 2007, 2019, 2026, 2028, 2034, 2037, 2040, 2046, 2051, 2052, 2064, 2072, 2082, 2088, 2096, 2097, 2099, 2110, 2111, 2127, 2139, 2150, 2156, 2163, 2171, 2181, 2183, 2185, 2187, 2189, 2206, 2209, 2211, 2235, 2242, 2246, 2247, 2249, 2251, 2260, 2261, 2269, 2280, 2285, 2290, 2296, 2303, 2304, 2307, 2311, 2312, 2315, 2316, 2320, 2321, 2326, 2342, 2344, 2349, 2370, 2373, 2375, 2393, 2397, 2399, 2400, 2417, 2419, 2422, 2426, 2429, 2433, 2454, 2459, 2463, 2486, 2487, 2489, 2490, 2495, 2501, 2511, 2515, 2534, 2539, 2552, 2571, 2599, 2600, 2604, 2617, 2618, 2622, 2626, 2630, 2637, 2646, 2653, 2658, 2664, 2668, 2685, 2694, 2700, 2702, 2713, 2721, 2722, 2724, 2732, 2733, 2740, 2744, 2755, 2760, 2766, 2767, 2770, 2782, 2787, 2788, 2793, 2805, 2818, 2819, 2827, 2832, 2834, 2835, 2837, 2843, 2872, 2873, 2908, 2931, 2957, 2984, 2992, 3001, 3006, 3016, 3018, 3023, 3031, 3039, 3041, 3043, 3044, 3045, 3059, 3064, 3065, 3085, 3086, 3091, 3095, 3099, 3115, 3123, 3125, 3126, 3127, 3139, 3143, 3160, 3161, 3164, 3171, 3172, 3173, 3187, 3191, 3193, 3200, 3204, 3210, 3223, 3227, 3230, 3248, 3249, 3258, 3265, 3268, 3271, 3273, 3274, 3302, 3308, 3313, 3314, 3319, 3320, 3328, 3332, 3344, 3352, 3357, 3365, 3377, 3380, 3386, 3404, 3405, 3416, 3421, 3425, 3426, 3427, 3432, 3433, 3439, 3440, 3449, 3453, 3476, 3485, 3504, 3512, 3518, 3519, 3525, 3533, 3534, 3542, 3555, 3556, 3562, 3563, 3566, 3567, 3577, 3588, 3593, 3602, 3623, 3629, 3630, 3647, 3648, 3654, 3681, 3682, 3683, 3692, 3694, 3697, 3702, 3708, 3713, 3715, 3716, 3717, 3720, 3733, 3746, 3758, 3779, 3783, 3785, 3803, 3806, 3807, 3808, 3809, 3810, 3820, 3835, 3845, 3846, 3850, 3852, 3859, 3862, 3863, 3868, 3877, 3880, 3891, 3896, 3902, 3903, 3908, 3910, 3912, 3916, 3932, 3952, 3961, 3967, 3973, 3978, 3983, 3985, 3986, 3989, 3992, 4003, 4010, 4013, 4020, 4023, 4030, 4032, 4040, 4053, 4058, 4064, 4094, 4095, 4099, 4100, 4101, 4102, 4110, 4112, 4114, 4116, 4118, 4123, 4126, 4133, 4143, 4152, 4154, 4156, 4157, 4163, 4164, 4167, 4168, 4177, 4184, 4187, 4192, 4194, 4200, 4208, 4213, 4220, 4224, 4233, 4235, 4239, 4241, 4247, 4248, 4260, 4262, 4263, 4270, 4271, 4287, 4290, 4303, 4304, 4306, 4315, 4319, 4329, 4331, 4338, 4356, 4364, 4369, 4379, 4381, 4382, 4383, 4402, 4403, 4414, 4415, 4423, 4424, 4427, 4432, 4435, 4444, 4445, 4448, 4451, 4452, 4453, 4455, 4458, 4461, 4462, 4471, 4474, 4487, 4491, 4495, 4503, 4508, 4527, 4535, 4539, 4540, 4550, 4554, 4560, 4564, 4582, 4593, 4600, 4603, 4605, 4607, 4627, 4635, 4641, 4648, 4663, 4664, 4676, 4695, 4698, 4704, 4705, 4708, 4710, 4712, 4718, 4722, 4726, 4730, 4733, 4735, 4740, 4747, 4748, 4752, 4753, 4754, 4756, 4765, 4784, 4788, 4789, 4798, 4800, 4802, 4809, 4818, 4822, 4831, 4834, 4835, 4842, 4846, 4849, 4854, 4855, 4860, 4862, 4867, 4870, 4875, 4880, 4887, 4889, 4897, 4899, 4902, 4909, 4912, 4915, 4922, 4941, 4948, 4952, 4954, 4959, 4960, 4968, 4974, 4975, 4976, 4984, 4992, 4998, 5000, 5002, 5005, 5007, 5009, 5012, 5019, 5031, 5034, 5038, 5039, 5055, 5057, 5060, 5062, 5068, 5071, 5079, 5080, 5081, 5082, 5085, 5089, 5095, 5096, 5103, 5112, 5115, 5119, 5125, 5130, 5132, 5161, 5163, 5166, 5172, 5175, 5177, 5183, 5185, 5193, 5194, 5210, 5223, 5227, 5233, 5238, 5241, 5245, 5249, 5254, 5266, 5273, 5274, 5279, 5280, 5293, 5295, 5302, 5303, 5307, 5314, 5316, 5320, 5335, 5336, 5348, 5360, 5361, 5362, 5364, 5373, 5386, 5394, 5400, 5406, 5407, 5415, 5419],
        15: [11, 15, 26, 32, 43, 44, 48, 61, 65, 68, 73, 76, 84, 93, 99, 100, 102, 105, 109, 123, 126, 136, 145, 151, 161, 163, 164, 172, 182, 184, 186, 188, 218, 224, 227, 228, 233, 235, 239, 245, 247, 251, 269, 291, 302, 303, 314, 318, 321, 338, 340, 344, 358, 374, 381, 389, 391, 409, 411, 413, 432, 434, 438, 443, 446, 457, 459, 463, 465, 471, 472, 478, 479, 485, 487, 495, 501, 504, 520, 535, 536, 545, 548, 550, 567, 569, 575, 579, 580, 587, 588, 589, 604, 608, 618, 624, 631, 632, 636, 638, 639, 641, 648, 661, 676, 688, 698, 701, 703, 707, 708, 731, 744, 746, 747, 760, 765, 768, 774, 778, 785, 801, 802, 805, 807, 812, 814, 824, 831, 836, 841, 855, 878, 897, 899, 908, 912, 922, 926, 931, 936, 945, 951, 970, 975, 987, 992, 993, 997, 1003, 1004, 1010, 1037, 1041, 1053, 1072, 1078, 1082, 1097, 1100, 1105, 1108, 1114, 1117, 1120, 1121, 1131, 1136, 1146, 1147, 1148, 1155, 1169, 1174, 1175, 1176, 1177, 1182, 1192, 1196, 1205, 1209, 1217, 1224, 1227, 1229, 1232, 1235, 1241, 1249, 1252, 1253, 1257, 1267, 1272, 1279, 1280, 1283, 1293, 1294, 1298, 1305, 1312, 1330, 1339, 1347, 1351, 1355, 1358, 1359, 1360, 1362, 1368, 1372, 1389, 1390, 1403, 1408, 1410, 1414, 1416, 1420, 1424, 1425, 1431, 1432, 1440, 1441, 1453, 1461, 1465, 1468, 1470, 1486, 1512, 1513, 1514, 1515, 1516, 1532, 1535, 1538, 1544, 1555, 1557, 1563, 1569, 1570, 1576, 1580, 1587, 1593, 1594, 1599, 1600, 1610, 1615, 1616, 1648, 1662, 1665, 1667, 1670, 1674, 1675, 1677, 1692, 1693, 1694, 1701, 1702, 1705, 1737, 1738, 1739, 1741, 1742, 1751, 1753, 1755, 1757, 1761, 1773, 1784, 1793, 1794, 1819, 1825, 1833, 1835, 1836, 1845, 1847, 1852, 1853, 1859, 1862, 1866, 1892, 1895, 1896, 1907, 1915, 1926, 1927, 1931, 1936, 1939, 1943, 1946, 1949, 1950, 1951, 1955, 1970, 1972, 1976, 1980, 1986, 1990, 2003, 2023, 2030, 2035, 2036, 2044, 2056, 2059, 2067, 2069, 2078, 2079, 2083, 2089, 2092, 2101, 2108, 2123, 2126, 2132, 2141, 2143, 2144, 2159, 2160, 2165, 2173, 2177, 2180, 2184, 2190, 2196, 2199, 2205, 2208, 2213, 2215, 2221, 2233, 2234, 2241, 2245, 2248, 2252, 2256, 2266, 2270, 2271, 2298, 2299, 2302, 2306, 2308, 2318, 2319, 2323, 2334, 2337, 2343, 2346, 2348, 2350, 2354, 2361, 2365, 2369, 2371, 2378, 2381, 2383, 2387, 2388, 2402, 2405, 2408, 2409, 2410, 2421, 2425, 2428, 2430, 2446, 2456, 2460, 2462, 2466, 2468, 2473, 2478, 2480, 2484, 2492, 2494, 2503, 2507, 2508, 2510, 2512, 2514, 2516, 2518, 2520, 2521, 2554, 2555, 2558, 2565, 2572, 2582, 2589, 2594, 2595, 2597, 2606, 2615, 2621, 2631, 2634, 2647, 2657, 2661, 2663, 2669, 2689, 2690, 2691, 2707, 2715, 2730, 2735, 2738, 2749, 2750, 2754, 2759, 2764, 2772, 2796, 2799, 2801, 2802, 2803, 2809, 2821, 2823, 2828, 2838, 2844, 2846, 2849, 2866, 2869, 2883, 2889, 2894, 2899, 2915, 2916, 2920, 2921, 2922, 2924, 2925, 2926, 2928, 2932, 2943, 2974, 2977, 2979, 2988, 2995, 3012, 3014, 3021, 3024, 3032, 3033, 3036, 3050, 3052, 3069, 3071, 3072, 3076, 3084, 3088, 3089, 3090, 3094, 3096, 3098, 3104, 3106, 3107, 3110, 3114, 3117, 3118, 3137, 3140, 3145, 3149, 3154, 3157, 3159, 3166, 3176, 3179, 3184, 3190, 3195, 3199, 3202, 3203, 3206, 3211, 3216, 3224, 3225, 3228, 3239, 3241, 3252, 3254, 3255, 3256, 3257, 3260, 3272, 3275, 3284, 3287, 3288, 3298, 3299, 3303, 3317, 3326, 3327, 3330, 3337, 3343, 3345, 3349, 3351, 3353, 3355, 3356, 3362, 3363, 3376, 3381, 3385, 3387, 3388, 3389, 3392, 3395, 3403, 3423, 3424, 3452, 3460, 3471, 3489, 3491, 3493, 3494, 3500, 3501, 3508, 3509, 3510, 3514, 3515, 3528, 3532, 3535, 3553, 3554, 3564, 3565, 3568, 3569, 3575, 3595, 3605, 3618, 3627, 3640, 3649, 3652, 3659, 3671, 3673, 3676, 3678, 3680, 3689, 3693, 3699, 3701, 3709, 3718, 3728, 3731, 3739, 3751, 3754, 3755, 3764, 3777, 3782, 3788, 3789, 3791, 3792, 3793, 3812, 3814, 3819, 3825, 3827, 3834, 3847, 3855, 3856, 3857, 3860, 3882, 3884, 3907, 3914, 3917, 3924, 3927, 3939, 3943, 3946, 3947, 3948, 3958, 3962, 3965, 3969, 3977, 3980, 3990, 4001, 4015, 4025, 4034, 4036, 4037, 4042, 4046, 4054, 4061, 4062, 4067, 4071, 4072, 4077, 4083, 4090, 4092, 4093, 4098, 4104, 4105, 4119, 4121, 4136, 4141, 4145, 4160, 4161, 4162, 4170, 4183, 4188, 4191, 4193, 4203, 4210, 4217, 4222, 4223, 4230, 4234, 4237, 4238, 4246, 4249, 4251, 4252, 4264, 4272, 4276, 4277, 4280, 4283, 4293, 4295, 4298, 4299, 4309, 4317, 4318, 4320, 4323, 4327, 4341, 4345, 4346, 4363, 4367, 4374, 4384, 4388, 4392, 4397, 4404, 4429, 4431, 4433, 4438, 4440, 4442, 4450, 4469, 4470, 4472, 4475, 4477, 4478, 4480, 4482, 4490, 4498, 4500, 4501, 4506, 4510, 4512, 4520, 4523, 4531, 4532, 4533, 4544, 4556, 4558, 4563, 4567, 4568, 4573, 4574, 4591, 4599, 4604, 4612, 4614, 4618, 4624, 4626, 4637, 4638, 4652, 4654, 4661, 4678, 4686, 4702, 4703, 4709, 4714, 4719, 4736, 4745, 4755, 4762, 4768, 4770, 4772, 4777, 4778, 4780, 4783, 4792, 4799, 4801, 4808, 4810, 4825, 4833, 4837, 4843, 4848, 4853, 4863, 4869, 4878, 4891, 4892, 4900, 4906, 4926, 4947, 4949, 4955, 4964, 4969, 4985, 4996, 5004, 5008, 5013, 5018, 5023, 5029, 5030, 5044, 5052, 5058, 5061, 5070, 5073, 5078, 5088, 5091, 5098, 5099, 5100, 5108, 5109, 5113, 5121, 5124, 5127, 5129, 5136, 5141, 5143, 5146, 5153, 5154, 5155, 5157, 5160, 5164, 5169, 5187, 5189, 5190, 5196, 5198, 5202, 5212, 5230, 5232, 5234, 5235, 5240, 5247, 5262, 5264, 5265, 5268, 5269, 5276, 5287, 5324, 5334, 5337, 5339, 5350, 5352, 5353, 5359, 5363, 5366, 5367, 5372, 5377, 5388, 5397, 5401, 5403, 5404, 5411, 5421, 5423]}


def FEMNIST_iid(dataset,num_users):
    args = args_parser()
    if  os.path.exists(args.private_dataset_index):
        print('private_dataset_index exist ~ ')
        f  = open(args.private_dataset_index,'r')
        temp = f.read()
        dict_users =eval(temp)
        return dict_users
    else:
        print('create private_dataset_index ~ ')
        # num_item = int(len(dataset) / num_users)
        num_class_item = 3  # 用于达到作者目的！
        dict_users = {}
        for i in range(num_users):
            dict_users[i]=set()
        for i in range(num_users):
            for key in dict.keys():
                temp = set(np.random.choice(dict[key], num_class_item, replace=False))
                dict_users[i] = dict_users[i] | temp
                dict[key] = list(set(dict[key]) - temp)
        f = open(args.private_dataset_index,'w')
        f.write(str(dict_users))
        f.close()
        return dict_users



def MNIST_random(dataset,epochs):
    num_item = 5000
    dict_epoch,all_idxs = {},[i for i in range(len(dataset))]
    for i in range(epochs):
        dict_epoch[i] = set(np.random.choice(all_idxs,num_item,replace=False))
        all_idxs = list(set(all_idxs)-dict_epoch[i])
    return dict_epoch

class args:
    dataset = 'mnist'
    private_dataset = 'FEMNIST'

# get_public_dataset(args)
# init_private_dataset(args)
# # data_train,data_test = get_private_dataset(args)
# data_train,data_test = get_private_dataset_balanced(args)
# print(FEMNIST_iid(data_train,10)[9])


# def generateIndex(dataset):
#     dict_private_index = {}
#     for i in range(len(dataset)):
#         dict_private_index.setdefault(data_train[i][1], []).append(i)
#     return dict_private_index
# print(generateIndex(data_train))

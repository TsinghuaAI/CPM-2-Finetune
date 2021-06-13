# CPM-2-Finetune

本仓库为 CPM-2 模型的 fine-tune 代码仓库，可以用于模型 Fine-tune 的多机多卡训练/测试。

CPM-2技术报告请参考[link](https://github.com/TsinghuaAI/tsinghuaai.github.io/blob/main/CPM-2.pdf)。



## 0 模型下载

请在智源资源[下载页面](https://resource.wudaoai.cn/home?ind=2&name=WuDao%20WenYuan&id=1394901846484627456)进行申请，文件介绍如下：

| 文件名 | 描述 | 参数大小 |
| :-----| :----: | :----: |
| 100000.tar | 纯中文模型 | 110亿 |
| 36000.tar | 中英文双语模型 | 110亿 |
| 300000.tar | 中英文MoE模型 | 1980亿 |


## 1 安装
可以直接拉取我们提供的 Docker 环境：

```[bash]
docker pull gyxthu17/cpm-2:1.0
```


## 2 运行

`scripts/full_model/` 目录下的 7 个 .sh 文件分别对应技术报告中 7 个数据集的 Fine-tune 脚本。注意：除了 wmt_cn 之外，其他数据集都使用**纯中文模型**，wmt_cn 数据集使用**中英双语模型**。

运行前，需要先将脚本中的 `WORKING_DIR` 改为此 CPM-2-Finetune 路径，将 `DATA_PATH` 改为数据集存储的目录，`CKPT_PATH` 改为模型权重所在的目录。可以设置 `SAVE_PATH` 指定训练结果存储的路径，将 `${WORKING_DIR}/configs/host_files/hostfile-cpm2` 中的 node-0 和 node-1 改为多机训练的主机名称。

使用以下命令运行，例如要进行 Math23K 数据集的 Fine-tune，则：

```[bash]
    bash scripts/finetune_t5_math.sh
```

## 3 引用

如果您使用了我们的代码，请您引用下面的文章。

```
@article{cpm-v2,
  title={CPM-2: Large-scale Cost-efficient Pre-trained Language Models},
  author={Zhang, Zhengyan and Gu, Yuxian and Han, Xu and Chen, Shengqi and Xiao, Chaojun and Sun, Zhenbo and Yao, Yuan and Qi, Fanchao and Guan, Jian and Ke, Pei and Cai, Yanzheng and Zeng, Guoyang and Tan, Zhixing and Liu, Zhiyuan and Huang, Minlie and Han, Wentao and Liu, Yang and Zhu, Xiaoyan and Sun, Maosong},
  year={2021}
}
```

# CPM-2-Finetune

[English Version](https://github.com/TsinghuaAI/CPM-2-Finetune/blob/master/README_en.md)

本仓库为 CPM-2 模型的 fine-tune 代码仓库，可以用于模型 Fine-tune 的多机多卡训练/测试。

CPM-2技术报告请参考[link](https://arxiv.org/abs/2106.10715)。


## 0 模型下载

请在智源资源[下载页面](https://resource.wudaoai.cn/home?ind=2&name=WuDao%20WenYuan&id=1394901846484627456)进行申请，文件介绍如下：

| 文件名 | 描述 | 参数大小 |
| :-----| :----: | :----: |
| 100000.tar | 纯中文模型 | 110亿 |
| 36000.tar | 中英文双语模型 | 110亿 |
| 300000.tar | 中英文MoE模型 | 1980亿 |

下载后的模型应该包含4个 .pt 文件：`mp_rank_0[0-3]_model_states.pt`。加载模型之前，需要先将这些文件放在名为 `100000/` 的目录下，目录外加上 `latest_checkpointed_iteration.txt` 文件，文件只有一行，内容是 100000。例如，若模型权重所在目录为 `cpm2/`，则目录结构为：

```
cpm2/
├── 100000
│   ├── mp_rank_00_model_states.pt
│   ├── mp_rank_01_model_states.pt
│   ├── mp_rank_02_model_states.pt
│   └── mp_rank_03_model_states.pt
└── latest_checkpointed_iteration.txt
```

## 1 安装
我们提供了两种安装的方式，其中，我们推荐直接使用 docker 以避免软件包版本的问题。

### 方式一：直接使用 Docker (推荐)
可以直接拉取我们提供的 Docker 环境：

```[bash]
docker pull gyxthu17/cpm-2:1.1
```

由于运行环境都已在 Docker 中配置好，因此不需要设置额外的环境变量。运行前需要将本目录挂载到 Docker 中，例如将本目录挂载到 Docker 中的 /mnt，可以使用以下命令运行 Docker 环境：
```[bash]
docker run -ti -v ${PWD}:/mnt gyxthu17/cpm-2:1.1 /bin/bash
```
Docker 启动之后在 /mnt 下操作即可。

### 方式二：配置 deepspeed

我们使用了`0.3.9`版本的 deepspeed，可根据其[仓库](https://github.com/microsoft/DeepSpeed/releases/tag/v0.3.9)提供的文档进行安装。由于 deepspeed 本身存在一些 bug，因此需要对其中的文件进行一些修改，原因可以参考 https://github.com/TsinghuaAI/CPM-2-Finetune/issues/11 。具体地，需要修改 `deepspeed/runtime/zero/stage1.py` 中的两行代码。我们在仓库中提供了修改后的 `stage1.py`，被修改的行标记了 `CPM: HACK`。 用仓库中的 `stage1.py` 替换 `deepspeed/runtime/zero/stage1.py` 即可完成修改。

**注意我们目前只修复了 deepspeed stage 1 的问题，其他优化方法可以按照同样方法进行修改**

## 2 全参数微调

`scripts/full_model/` 目录下的 7 个 .sh 文件分别对应技术报告中 7 个数据集的 Fine-tune 脚本。注意：除了 wmt_cn 之外，其他数据集都使用**纯中文模型**，wmt_cn 数据集使用**中英双语模型**。

运行前，需要先将脚本中的 `WORKING_DIR` 改为此 CPM-2-Finetune 文件夹的路径，将 `DATA_PATH` 改为数据集存储的目录，`CKPT_PATH` 改为模型权重所在的目录。可以设置 `SAVE_PATH` 指定训练结果存储的路径，将 `${WORKING_DIR}/configs/host_files/hostfile-cpm2` 中的 node-0 和 node-1 改为多机训练的主机名称。

使用以下命令运行，例如要进行 Math23K 数据集的 Fine-tune，则：

```[bash]
cd CPM-2-Finetune
bash scripts/full_model/finetune_cpm2_math.sh
```

## 3 基于 Prompt 的微调

`scripts/prompt/` 目录下的 7 个 .sh 文件分别对应技术报告中 7 个数据集的 Prompt-based Tuning 脚本。注意：除了 wmt_cn 之外，其他数据集都使用**纯中文模型**，wmt_cn 数据集使用**中英双语模型**。

与全参数微调相同，运行前需要修改 `WORKING_DIR`、`DATA_PATH`、`CKPT_PATH` 和 `SAVE_PATH` 以及 `${WORKING_DIR}/configs/host_files/hostfile-cpm2` 文件。

除此之外，还可以通过修改 `configs/prompt/` 中的配置文件修改 prompt 的插入位置等配置信息。例如，对于 lcqmc 数据集，`configs/prompt/lcqmc` 目录下提供了多个 prompt 插入位置的 .json 配置文件。举例来说，lcqmc_33_34_33 代表输入的两个句子构成的三个可能位置插入 prompt 的比例为 33:34:33。`finetune_cpm2_lcqmc.sh` 中的 `PROMPT_CONFIG` 变量显式引用了这些文件。

最后，使用以下命令运行：

```[bash]
cd CPM-2-Finetune
bash scripts/prompt/finetune_cpm2_lcqmc.sh
```

## 4 引用

如果您使用了我们的代码，请您引用下面的文章。

```
@article{cpm-v2,
  title={CPM-2: Large-scale Cost-efficient Pre-trained Language Models},
  author={Zhang, Zhengyan and Gu, Yuxian and Han, Xu and Chen, Shengqi and Xiao, Chaojun and Sun, Zhenbo and Yao, Yuan and Qi, Fanchao and Guan, Jian and Ke, Pei and Cai, Yanzheng and Zeng, Guoyang and Tan, Zhixing and Liu, Zhiyuan and Huang, Minlie and Han, Wentao and Liu, Yang and Zhu, Xiaoyan and Sun, Maosong},
  year={2021}
}
```

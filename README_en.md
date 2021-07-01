# CPM-2-Finetune

[中文版](https://github.com/TsinghuaAI/CPM-2-Finetune/blob/master/README.md)

This is the repository of the fine-tuning code for CPM-2 which can be used for multi-node training and testing.

Please refer to the [technical report](https://arxiv.org/abs/2106.10715) for the details of CPM-2.


## 0 Pre-trained Weights

Please apply for the pre-trained weights of CPM-2 model on the resource downloading page of BAAI ([link](https://resource.wudaoai.cn/home?ind=2&name=WuDao%20WenYuan&id=1394901846484627456)). The descriptions of the files are as follows:

| File Name  | Description                    | Model Size |
| ---------- | ------------------------------ | ---------- |
| 100000.tar | Chinese Model                  | 11B        |
| 36000.tar  | Chinese-English Model          | 11B        |
| 300000.tar | Chinese-English Model with MoE | 198B       |

The downloaded model weight consists of 4 .pt files: `mp_rank_0[0-3]_model_states.pt`. Before loading the model, you need to put the files unfer the directory named `100000/`. Then, create a file `latest_checkpointed_iteration.txt` which contain only one line for a number: 100000. For example, assume the directory for the model weight is `cpm2/`, then the structure of the directory is:

```
cpm2/
├── 100000
│   ├── mp_rank_00_model_states.pt
│   ├── mp_rank_01_model_states.pt
│   ├── mp_rank_02_model_states.pt
│   └── mp_rank_03_model_states.pt
└── latest_checkpointed_iteration.txt
```

## 1 Installation

For installation, you can directly pull our docker environment:

```bash
docker pull gyxthu17/cpm-2:1.0
```

Run the following code to run the docker image:
```[bash]
docker run -ti gyxthu17/cpm-2:1.0 /bin/bash
```

## 2 Full Model Fine-tuning

The scripts of full model fine-tuning are under `scripts/full_model/`. The 7 .sh files are used for the 7 downstream tasks in our report respectively. NOTE: we use the **Chinese-English Model** for the wmt\_cn dataset and the **Chinese Model** for other datasets.

Before running the code, please change `WORKING_DIR` in the script to the path of this CPM-2-Finetune directory, change `DATA_PATH` to the path where the datasets are stored, and `CKPT_PATH` to the path where the pre-trained weights are stored. You can also change `SAVE_PATH` to the path where the results are saved. For the multi-node setting, you need to change node-0 and node-1 in `${WORKING_DIR}/configs/host_files/hostfile-cpm2` to the node names where you run distributed training. 

Run the following code to fine-tune the model. For example, to fine-tune the Math23K dataset, run:

```bash
cd CPM-2-Finetune
bash scripts/full_model/finetune_cpm2_math.sh
```



## 3 Prompt-Based Fine-tuning

The scripts of prompt-based fine-tuning are under `scripts/prompt/`. The 7 .sh files are used for the 7 downstream tasks in our report respectively. NOTE: we use the **Chinese-English Model** for the wmt\_cn dataset and the **Chinese Model** for other datasets.

Similar to full model fine-tuning, you need to change `WORKING_DIR`, `DATA_PATH`, `CKPT_PATH`, and `SAVE_PATH` in the scripts as well as the node names in `${WORKING_DIR}/configs/host_files/hostfile-cpm2` for distributed training.

Besides, you can modify the configuration files in `configs/prompt/` to try different strategies to use the prompt such as the position to insert the prompt tokens. For example, for the LCQMC dataset, there are many JSON files for configuration under `configs/prompt/lcqmc`. Taking lcqmc\_33\_34\_33.json as an example, this file indicates that we insert prompt tokens at the three possible positions (Front, Middle, Back) of the two sentences and the ratio of the prompt token number of the three positions is 33:34:33. You can specify the variable `PROMPT_CONFIG` in `finetune_cpm2_lcqmc.sh` to the path of the configuration file.

Run the following code to fine-tune the model:

```bash
cd CPM-2-Finetune
bash scripts/prompt/finetune_cpm2_lcqmc.sh
```



## 4 Reference

If you use the code, please cite the following paper:

```
@article{cpm-v2,
 title={CPM-2: Large-scale Cost-efficient Pre-trained Language Models},
 author={Zhang, Zhengyan and Gu, Yuxian and Han, Xu and Chen, Shengqi and Xiao, Chaojun and Sun, Zhenbo and Yao, Yuan and Qi, Fanchao and Guan, Jian and Ke, Pei and Cai, Yanzheng and Zeng, Guoyang and Tan, Zhixing and Liu, Zhiyuan and Huang, Minlie and Han, Wentao and Liu, Yang and Zhu, Xiaoyan and Sun, Maosong},
 year={2021}
}
```






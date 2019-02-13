# Behavioral Cloning in Udacity Simulator
This repo documents my work on training a CNN model for self-driving car. I use the simulator developed by Udacity for car driving. I deployed fastai framework for model training. I experimented with different models, the first two being pretrained ResNet34 and the CNN proposed by NVIDIA in literature.

## Design
*drive.py*: load in trained model and drive the car in simulator<br/>
*log_file.py*: helper functions applied on log file<br/>
*img_folder.py*: helper functions applied on image folder<br/>
*img_process.py*: applied *log_file.py* and *img_folder.py* for image processing.<br/>
*model_resnet34.ipynb*: first attempt in training resnet34 by fastai v1.0 on Google Colab<br/>

## References
1. [literature] [End to End Learning for Self-driving Car" - NVIDIA](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf)
2. [literature] [Wide Residual Networks](https://arxiv.org/abs/1605.07146)
3. [medium] [behavioral cloning transfer learning with feature extraction](https://medium.com/@kastsiukavets.alena/behavioral-cloning-transfer-learning-with-feature-extraction-a17b0ebabf67)
4. [github] [the github repo of 3. by Helen1987](https://github.com/Helen1987/CarND-Behavioral-Cloning-P3)
5. [medium] [6 different end-to-end neural networks](https://medium.com/self-driving-cars/6-different-end-to-end-neural-networks-f307fa2904a5?fbclid=IwAR1aZ2OWA8adivjcIUAf1XWF2T4T3RuWmZQDShk-rY6gvhJfPCMbydL1DqM)

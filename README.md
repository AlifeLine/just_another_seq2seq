
*A lot of Chinese in codes and docs*

# Just another seq2seq repo

- [x] 主要是从个人角度梳理了一下seq2seq的代码
- [x] 加入了可选基本的CRF支持，loss和infer（还不确定对
- [x] 加入了一些中文注释
- [x] 相对于其他一些repo，bug可能会少一些
    - 有些repo的实现在不同参数下会有问题：例如有些支持gru不支持lstm，有些不支持bidirectional，有些选择depth > 1的时候会有各种bug之类的，这些问题我都尽量修正了，虽然不保证实现肯定是对的
- [x] 后续我可能会添加一些中文的例子，例如对联、古诗、闲聊、NER
- [x] 根据本repo，我会整理一份seq2seq中间的各种trick和实现细节的坑
    - [参考这里](https://github.com/qhduan/ConversationalRobotDesign/tree/master/%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA%EF%BC%9A%E7%A5%9E%E7%BB%8F%E5%AF%B9%E8%AF%9D%E6%A8%A1%E5%9E%8B%E7%9A%84%E5%AE%9E%E7%8E%B0%E4%B8%8E%E6%8A%80%E5%B7%A7)
- [ ] pretrained embedding support
- [ ] 后续这个repo会作为一个基础完成一个dialogue system
    - seq2seq模型至少可以作为通用NER实现
    - 截止2018年初，最好的NER应该还是bi-LSTM + CRF，也有不加CRF效果好的
    - 当然这个不完全算seq2seq啦

# Update Log

2018-03-06

增加了chatbot中anti-lm的训练方法样例，在`chatbot/train_anti.py`中。
这个模式参考了[Li et al., 2015](https://arxiv.org/pdf/1510.03055v3.pdf)和代码
[Marsan-Ma/tf_chatbot_seq2seq_antilm](https://github.com/Marsan-Ma/tf_chatbot_seq2seq_antilm)。  

加入anti-lm来看，diversity是有提高，不过整体来看，并不是说就很好好。
但是明显降低了机器回答“我不知道”和“我不知道你在说什么”这样的语言概率。

虽然我在不同的地方在还尝试实现了下面这两个（其实都是一个人写的啦）
[Li et al., 2016](https://arxiv.org/abs/1606.01541)
[Li et al., 2017](https://arxiv.org/abs/1701.06547)
不过基本上不太成功的感觉，虽然我也没做太严格的做法。

# Known issues

Example里的例子和整个项目，虽然未经验证，但是在内存较小的电脑上（<8GB），可能会有问题。
这涉及到数据处理、数据输入、模型参数等部分，所以严格来说并不算BUG。

# Platform

作者在一台64GB内存 + GTX1070 6GB + Ubuntu 16.04电脑上运行。

内存肯定不需要这么大，不过显存如果在2GB，如果要在GPU上运行模型，可能需要调节batch_size等模型参数。

# Example

Example里面用到的数据，都是比较小且粗糙的。
作者只基本验证了可行性，所以也不可能实用了，例如英汉翻译就别期待准确率很高了，
大概意思到了就代表模型的一定有效性了。

[英汉句子翻译实例](/en2zh/)

#### 测试结果样例

***我不保证能重复实现能得到一模一样的结果***

```
Input English Sentence:go to hell
[[30475 71929 33464]] [3]
[[41337 48900 41337 44789     3]]
['go', 'to', 'hell']
['去', '地狱', '去', '吧', '</s>']
Input English Sentence:nothing, but the best for you
[[50448   467 13008 71007 10118 27982 79204]] [7]
[[ 25904 132783  90185      4  28145  81577  80498  28798      3]]
['nothing', ',', 'but', 'the', 'best', 'for', 'you']
['什么', '都', '没有', ' ', '但', '最好', '是', '你', '</s>']
Input English Sentence:i'm a bad boy
[[35437   268  4018  8498 11775]] [5]
[[ 69313  80498  21899  49069 100342      3     -1]]
['i', "'m", 'a', 'bad', 'boy']
['我', '是', '个', '坏', '男孩', '</s>', '<unk>']
Input English Sentence:i'm really a bad boy
[[35437   268 58417  4018  8498 11775]] [6]
[[ 69313 103249  80498  17043  49069 100342      3      3      3      3
       3      3]]
['i', "'m", 'really', 'a', 'bad', 'boy']
['我', '真的', '是', '一个', '坏', '男孩', '</s>', '</s>', '</s>', '</s>', '</s>', '</s>']
```


[NER实例](/ner/)

[Chatbot实例](/chatbot/)

[Chatbot Adversarial实例](/chatbot_ad/)

# TensorFlow alert

Test in

```python
import tensorflow as tf
tf.__version__ >= '1.4.0' and tf.__version__ <= '1.5.0'
```

TensorFlow的API总是变，不能保证后续的更新兼容

本repo本质是一个学习性质的repo，作者只是希望尽量保持代码的整齐、理解、可读，并不对不同平台（尤其windows）的兼容，或者后续更新做保证，对不起

# Related work

As mention in the head of `sequence_to_sequence.py`,
At beginning, the code is heavily borrow from [here](https://github.com/JayParks/tf-seq2seq/blob/master/seq2seq_model.py)

I have modified a lot of code, some ***Chinese comments*** in the code.
And fix many bugs, restructure many things, add more features.

Code was borrow heavily from:

https://github.com/JayParks/tf-seq2seq/blob/master/seq2seq_model.py

Another wonderful example is:

https://github.com/Marsan-Ma/tf_chatbot_seq2seq_antilm

Official sequence2sequence tutorial

https://www.tensorflow.org/tutorials/seq2seq

Official sequence2sequence project:

https://github.com/tensorflow/nmt

Another official sequence2sequence model:

https://github.com/tensorflow/tensor2tensor

Another seq2seq repo:

https://github.com/ematvey/tensorflow-seq2seq-tutorials


# pylint

pylintrc from [here](https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/tools/ci_build/pylintrc)

changed indent from 2 to 4

PS. 谷歌的lint一般建议indent是2，相反百度的lint很多建议indent是4，
个人怀疑这里面有“中文”的问题，也许是因为从小习惯作文空两格？（就是四个英文空格了）

我个人是习惯4个的


# Chatbot测试

## 1、下载数据

Subtitle data from [here](https://github.com/fateleak/dgk_lost_conv)

```
wget https://github.com/fateleak/dgk_lost_conv/raw/master/dgk_shooter_min.conv.zip
```

输出：`dgk_shooter_min.conv.zip`

## 2、解压缩

```
unzip dgk_shooter_min.conv.zip
```

输出：`dgk_shooter_min.conv`

## 3、预处理数据

```
python3 extract_conv.py
```

输出：`chatbot.pkl`

## 4、训练数据

运行 `python3 train.py` 训练（默认到`./s2ss_chatbot.ckpt`）

## 5、测试数据（测试对话）

运行 `python3 test.py` 查看测试结果

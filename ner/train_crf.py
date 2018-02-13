"""
对RNNCRF模型进行基本的参数组合测试
"""

import sys
import random
import pickle

import numpy as np
import tensorflow as tf
from tqdm import tqdm

sys.path.append('..')


def test(bidirectional, cell_type, depth,
         use_residual, use_dropout, time_major, hidden_units,
         output_project_active):
    """测试不同参数在生成的假数据上的运行结果"""

    from rnn_crf import RNNCRF
    from data_utils import batch_flow_bucket
    from word_sequence import WordSequence # pylint: disable=unused-variable

    x_data, y_data, ws_input, ws_target = pickle.load(
        open('ner.pkl', 'rb'))

    # 获取一些假数据
    # x_data, y_data, ws_input, ws_target = generate(size=10000)

    # 训练部分
    split = int(len(x_data) * 0.8)
    x_train, x_test, y_train, y_test = (
        x_data[:split], x_data[split:], y_data[:split], y_data[split:])
    n_epoch = 10
    batch_size = 128
    steps = int(len(x_train) / batch_size) + 1

    config = tf.ConfigProto(
        # device_count={'CPU': 1, 'GPU': 0},
        allow_soft_placement=True,
        log_device_placement=False
    )

    save_path = '/tmp/s2ss_ner_crf.ckpt'

    tf.reset_default_graph()
    with tf.Graph().as_default():
        random.seed(0)
        np.random.seed(0)
        tf.set_random_seed(0)

        with tf.Session(config=config) as sess:

            model = RNNCRF(
                input_vocab_size=len(ws_input),
                target_vocab_size=len(ws_target),
                max_decode_step=100,
                batch_size=batch_size,
                learning_rate=0.001,
                bidirectional=bidirectional,
                cell_type=cell_type,
                depth=depth,
                use_residual=use_residual,
                use_dropout=use_dropout,
                parallel_iterations=64,
                hidden_units=hidden_units,
                optimizer='adam',
                time_major=time_major,
                output_project_active=output_project_active
            )
            init = tf.global_variables_initializer()
            sess.run(init)

            # print(sess.run(model.input_layer.kernel))
            # exit(1)

            flow = batch_flow_bucket(
                x_train, y_train, ws_input, ws_target, batch_size
            )

            for epoch in range(1, n_epoch + 1):
                costs = []
                bar = tqdm(range(steps), total=steps,
                           desc='epoch {}, loss=0.000000'.format(epoch))
                for _ in bar:
                    x, xl, y, yl = next(flow)
                    cost = model.train(sess, x, xl, y, yl)
                    costs.append(cost)
                    bar.set_description('epoch {} loss={:.6f}'.format(
                        epoch,
                        np.mean(costs)
                    ))

            model.save(sess, save_path)

    # 测试部分

    tf.reset_default_graph()
    model_pred = RNNCRF(
        input_vocab_size=len(ws_input),
        target_vocab_size=len(ws_target),
        max_decode_step=100,
        batch_size=1,
        mode='decode',
        bidirectional=bidirectional,
        cell_type=cell_type,
        depth=depth,
        use_residual=use_residual,
        use_dropout=use_dropout,
        hidden_units=hidden_units,
        time_major=time_major,
        parallel_iterations=1,
        output_project_active=output_project_active
    )
    init = tf.global_variables_initializer()

    with tf.Session(config=config) as sess:
        sess.run(init)
        model_pred.load(sess, save_path)

        bar = batch_flow_bucket(x_test, y_test, ws_input, ws_target, 1)
        t = 0
        for x, xl, y, yl in bar:
            pred = model_pred.predict(
                sess,
                np.array(x),
                np.array(xl)
            )
            print(ws_input.inverse_transform(x[0]))
            print(ws_target.inverse_transform(y[0]))
            print(ws_target.inverse_transform(pred[0]))
            t += 1
            if t >= 30:
                break


def main():
    """入口程序，开始测试不同参数组合"""
    random.seed(0)
    np.random.seed(0)
    tf.set_random_seed(0)
    test(True, 'lstm', 1, False, True, False, 64, 'tanh')


if __name__ == '__main__':
    main()

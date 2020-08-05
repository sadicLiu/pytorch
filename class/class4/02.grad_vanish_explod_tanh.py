import torch
import torch.nn as nn

from common_tools import set_seed

set_seed(1)  # 设置随机种子

"""使用100层的全连接网络来演示梯度消失与梯度爆炸的问题 
    从运行结果可以看到,对每一层的参数随机初始化之后,每一层输出结果的方差都在变大,
    这就导致梯度爆炸的产生.
    因此,要想解决梯度消失和梯度爆炸的问题,就要保证每层输出数据的标准差数值合理
    
    对于全连接层,若神经元个数为n,使用标准正态分布初始化,可以推导出输出数据的方差为n
"""


class MLP(nn.Module):
    def __init__(self, neural_num, layers):
        super(MLP, self).__init__()
        self.linears = nn.ModuleList([nn.Linear(neural_num, neural_num, bias=False) for i in range(layers)])
        self.neural_num = neural_num

    def forward(self, x):
        for (i, linear) in enumerate(self.linears):
            x = linear(x)
            x = torch.tanh(x)

            print("layer:{}, std:{}".format(i, x.std()))
            if torch.isnan(x.std()):
                print("output is nan in {} layers".format(i))
                break

        return x

    def initialize(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                tanh_gain = nn.init.calculate_gain('tanh')

                # 手动计算并进行初始化
                # a = np.sqrt(6 / (self.neural_num + self.neural_num))
                # a *= tanh_gain
                # nn.init.uniform_(m.weight.data, -a, a)

                # 使用PyTorch提供的方法初始化
                nn.init.xavier_uniform_(m.weight.data, gain=tanh_gain)
                # nn.init.xavier_normal_(m.weight.data, gain=tanh_gain)


layer_nums = 100
neural_nums = 256
batch_size = 16

net = MLP(neural_nums, layer_nums)
net.initialize()

inputs = torch.randn((batch_size, neural_nums))  # normal: mean=0, std=1

output = net(inputs)
print(output)

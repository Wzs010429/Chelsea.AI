import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from tqdm import tqdm  # 导入tqdm
import matplotlib.pyplot as plt

class GCN(torch.nn.Module):
    def __init__(self, num_node_features, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_node_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)

        return torch.log_softmax(x, dim=1)

# 假设有4个节点，每个节点有3个特征
x = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], dtype=torch.float)

# 边索引
edge_index = torch.tensor([[0, 1, 2, 3, 0], [1, 2, 3, 0, 2]], dtype=torch.long)

# 节点标签
labels = torch.tensor([0, 1, 0, 1], dtype=torch.long)

# 假设我们将前两个节点用于训练，后两个用于测试
train_mask = torch.tensor([True, True, False, False], dtype=torch.bool)

# 更新Data对象以包含train_mask
data = Data(x=x, edge_index=edge_index, y=labels, train_mask=train_mask)

# 创建模型实例
model = GCN(num_node_features=3, num_classes=2)

# 定义损失函数和优化器
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 初始化用于记录训练损失的列表
loss_values = []

# 训练模型
for epoch in tqdm(range(200), desc="Training Progress"):
    optimizer.zero_grad()
    out = model(data)
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

    # 记录损失值
    loss_values.append(loss.item())

    # 打印损失值
    if (epoch + 1) % 10 == 0:  # 每10个epoch打印一次
        print(f'Epoch {epoch + 1}/{200}, Loss: {loss.item()}')

# 绘制损失曲线
plt.plot(loss_values, label='Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Over Time')
plt.legend()
plt.show()

import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from collections import defaultdict
import json
from torch_geometric.data import Data
import random

# 读取JSON文件
with open('fake_data.json', 'r') as file:
    data_json = json.load(file)

# 为UserID和PropertyID创建映射
node_mapping = {}
node_counter = 0
positive_edges = set()

for entry in data_json:
    user_id = entry["UserID"]
    if user_id not in node_mapping:
        node_mapping[user_id] = node_counter
        node_counter += 1

    for issue in entry["Conversation"]:
        if issue not in node_mapping:
            node_mapping[issue] = node_counter
            node_counter += 1

        # 记录正样本边
        positive_edges.add((node_mapping[user_id], node_mapping[issue]))

# 生成负样本边
negative_edges = set()
while len(negative_edges) < len(positive_edges):
    u = random.randint(0, len(node_mapping) - 1)
    v = random.randint(0, len(node_mapping) - 1)
    if u != v and (u, v) not in positive_edges and (v, u) not in positive_edges:
        negative_edges.add((u, v))

# 创建边和边标签
all_edges = list(positive_edges) + list(negative_edges)
edge_labels = [1] * len(positive_edges) + [0] * len(negative_edges)

# 转换为PyTorch张量
edge_index = torch.tensor(all_edges, dtype=torch.long).t().contiguous()
edge_labels = torch.tensor(edge_labels, dtype=torch.float32)

# 创建节点特征（这里使用简单的one-hot编码）
x = torch.eye(len(node_mapping))

# 构建图数据对象
data = Data(x=x, edge_index=edge_index, y=edge_labels)
print(data)
# 定义GCN模型
class GCN(torch.nn.Module):
    def __init__(self, num_features, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, hidden_channels)  # 新增一个GCN层
        self.out = torch.nn.Linear(hidden_channels, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = self.conv3(x, edge_index)  # 使用新增的GCN层
        x = F.relu(x)
        x = self.out(x)
        return torch.sigmoid(x)

# 设置设备，定义模型和优化器
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GCN(num_features=data.num_features, hidden_channels=64).to(device)
data = data.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# 定义二元交叉熵损失函数
criterion = torch.nn.BCELoss()

# 现在我们使用模型输出来计算边的预测
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)

    # 使用点积来生成边的特征
    edge_out = torch.sum(out[data.edge_index[0]] * out[data.edge_index[1]], dim=1)

    loss = criterion(edge_out, data.y)
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    edge_predictions = model(data.x, data.edge_index)

    # 使用点积来生成边的预测
    edge_predictions = torch.sum(out[data.edge_index[0]] * out[data.edge_index[1]], dim=1)

user_issue_predictions = defaultdict(list)
for i, edge in enumerate(data.edge_index.t()):
    user_idx, issue_idx = edge.tolist()
    prediction = edge_predictions[i].item()
    user_issue_predictions[user_idx].append((issue_idx, prediction))

# 为每个用户选出前5个问题
top_5_issues_per_user = {}
for user_idx, predictions in user_issue_predictions.items():
    sorted_issues = sorted(predictions, key=lambda x: x[1], reverse=True)
    top_5_issues = sorted_issues[:5]
    top_5_issues_per_user[user_idx] = top_5_issues

# 输出每个用户的前5个问题
for user_idx, issues in top_5_issues_per_user.items():
    print(f"User {user_idx}:")
    for issue_idx, prediction in issues:
        print(f"  Issue {issue_idx} with prediction score: {prediction}")

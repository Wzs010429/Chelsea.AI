import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from collections import defaultdict
import json
from torch_geometric.data import Data

# 读取JSON文件
with open('fake_data.json', 'r') as file:
    data_json = json.load(file)

# 为UserID和PropertyID创建映射
node_mapping = {}
node_counter = 0
edge_list = []

for entry in data_json:
    user_id = entry["UserID"]
    if user_id not in node_mapping:
        node_mapping[user_id] = node_counter
        node_counter += 1

    for issue in entry["Conversation"]:
        if issue not in node_mapping:
            node_mapping[issue] = node_counter
            node_counter += 1

        edge_list.append([node_mapping[user_id], node_mapping[issue]])

# 创建边索引
edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()

# 创建节点特征（这里使用简单的one-hot编码）
num_nodes = len(node_mapping)
x = torch.eye(num_nodes)

# 构建图数据对象
data = Data(x=x, edge_index=edge_index)

# print(data)

class GCN(torch.nn.Module):
    def __init__(self, num_features, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.out = torch.nn.Linear(hidden_channels, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = self.out(x)
        return torch.sigmoid(x)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GCN(num_features=data.num_features, hidden_channels=64).to(device)
data = data.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# 定义二元交叉熵损失函数
criterion = torch.nn.BCELoss()


model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    # 计算损失，假设data.y是边存在与否的标签
    loss = criterion(out[data.edge_index], data.y)
    loss.backward()
    optimizer.step()


model.eval()
with torch.no_grad():
    edge_predictions = model(data.x, data.edge_index)

# edge_predictions 包含了每条边的预测权重或概率

# 将预测转换为用户和问题的映射
user_issue_predictions = defaultdict(list)
for i, edge in enumerate(data.edge_index.t()):
    user_idx, issue_idx = edge.numpy()
    prediction = edge_predictions[i].item()
    user_issue_predictions[user_idx].append((issue_idx, prediction))

# 为每个用户选出前5个问题
top_5_issues_per_user = {}
for user_idx, predictions in user_issue_predictions.items():
    # 根据预测的权重或概率排序
    sorted_issues = sorted(predictions, key=lambda x: x[1], reverse=True)
    # 选择前5个
    top_5_issues = sorted_issues[:5]
    # 存储结果
    top_5_issues_per_user[user_idx] = top_5_issues

# 输出每个用户的前5个问题
for user_idx, issues in top_5_issues_per_user.items():
    print(f"User {user_idx}:")
    for issue_idx, prediction in issues:
        print(f"  Issue {issue_idx} with prediction score: {prediction}")
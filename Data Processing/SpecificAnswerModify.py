import AnswerGeneration
import csv

def update_csv_answers(filename, issue_name):
    updated_data = []

    # 读取 CSV 文件并查找匹配的行
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Issue'] == issue_name:
                # 调用 answer_generation 函数生成新答案
                # 假设 'data' 是您需要的数据，您需要根据实际情况调整
                new_answer = AnswerGeneration.answer_generation(data, row['Question'])
                row['Answer'] = new_answer
            updated_data.append(row)

    # 将更新的数据写回 CSV 文件
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=updated_data[0].keys())
        writer.writeheader()
        writer.writerows(updated_data)


data = """"""

# function call
# update_csv_answers()
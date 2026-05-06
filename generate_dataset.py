import os
import csv
import random

random.seed(42)
os.makedirs('data', exist_ok=True)
header = ['CustomerID','Gender','Age','Annual Income (k$)','Spending Score (1-100)']
rows = []
for i in range(1, 61):
    rows.append([i, random.choice(['Male','Female']), random.randint(18,35), random.randint(15,45), random.randint(60,100)])
for i in range(61, 121):
    rows.append([i, random.choice(['Male','Female']), random.randint(18,40), random.randint(45,80), random.randint(10,55)])
for i in range(121, 161):
    rows.append([i, random.choice(['Male','Female']), random.randint(36,60), random.randint(40,70), random.randint(40,85)])
for i in range(161, 201):
    rows.append([i, random.choice(['Male','Female']), random.randint(45,70), random.randint(70,140), random.randint(15,60)])

with open('data/mall_customers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print('Created data/mall_customers.csv with', len(rows), 'rows')

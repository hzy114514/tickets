import matplotlib.pyplot as plt

# ====================== 1. 四组原始实验数据 ======================
# 第1组 Pin=402
U1 = [0.1,0.26, 0.61, 1.22, 1.76, 1.89, 1.97, 2.00, 2.02, 2.04, 2.06, 2.07, 2.08, 2.09, 2.10, 2.10, 2.10, 2.11, 2.11, 2.11,2.12]
I1 = [44.9,44.9, 44.7, 44.4, 43.3, 39.8, 34.1, 31.0, 28.3, 26.0, 22.9, 20.5, 18.0, 16.4, 13.1, 12.0, 11.3, 9.1, 9.6, 9.9,0.1]

# 第2组 Pin=314
U2 = [0.1,0.47, 0.91, 1.53, 1.71, 1.83, 1.88, 1.91, 1.94, 1.97, 1.99, 2.00, 2.01, 2.02, 2.03, 2.03, 2.04, 2.06, 2.07, 2.06, 2.06,2.09]
I2 = [34.8,34.8, 34.6, 34.4, 33.5, 30.9, 29.0, 26.8, 24.8, 22.7, 20.7, 18.8, 17.4, 16.3, 15.6, 14.5, 13.6, 9.7, 8.8, 9.4, 9.8,0.1]

# 第3组 Pin=222
U3 = [0.1,0.37, 0.59, 0.78, 0.91, 1.00, 1.13, 1.32, 1.47, 1.59, 1.75, 1.85, 1.89, 1.91, 1.93, 1.95, 1.98, 1.99, 2.00, 2.01,2.02,2.04]
I3 = [24.7,24.7, 24.6, 24.5, 24.5, 24.4, 24.3, 24.3, 24.2, 23.9, 22.6, 19.9, 18.1, 17.1, 15.5, 14.1, 12.2, 10.6, 9.7, 8.7, 8.5,0.1]

# 第4组 Pin=132
U4 = [0.1,0.22, 0.44, 0.62, 0.74, 0.83, 0.87, 0.97, 1.05, 1.10, 1.16, 1.26, 1.34, 1.46, 1.58, 1.64, 1.71, 1.75, 1.81, 1.89, 1.96,2.0]
I4 = [14.8,14.8, 14.7, 14.7, 14.6, 14.5, 14.5, 14.5, 14.4, 14.4, 14.4, 14.4, 14.4, 14.2, 13.9, 13.5, 12.9, 12.3, 10.8, 9.3, 6.7,0.1]

Pin_list = [402, 314, 222, 132]
U_list = [U1, U2, U3, U4]
I_list = [I1, I2, I3, I4]

# ====================== 2. 计算函数 ======================
def calc_R_P(U, I):
    R = [u / (i / 1000) for u, i in zip(U, I)]
    P = [u * i for u, i in zip(U, I)]
    return R, P

def calc_all_params(U, I, Pin):
    R, P = calc_R_P(U, I)
    Pmax = max(P)
    idx = P.index(Pmax)
    Um, Im, Ropt = U[idx], I[idx], R[idx]

    Is = I[0]
    U0 = U[-1]
    U0_Is = U0 * Is
    Ri = U0 / (Is / 1000)
    ratio = Ropt / Ri
    FF = Pmax / U0_Is
    eta = Pmax / Pin * 100
    return [Pin, Pmax, U0_Is, Ropt, Ri, ratio, FF, eta]

R_list, P_list, result_data = [], [], []
for i in range(4):
    R, P = calc_R_P(U_list[i], I_list[i])
    R_list.append(R)
    P_list.append(P)
    result_data.append(calc_all_params(U_list[i], I_list[i], Pin_list[i]))

# 设置中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ====================== 3. 图1：I-U + R-P 双曲线图 ======================
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 10), dpi=100)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
labels = ['组1 $P_{in}$=402', '组2 $P_{in}$=314', '组3 $P_{in}$=222', '组4 $P_{in}$=132']
marks = ['o-', 's-', '^-', 'd-']

for i in range(4):
    ax1.plot(U_list[i], I_list[i], marks[i], color=colors[i], label=labels[i], linewidth=1.5, markersize=3)
ax1.set_xlabel('端电压 $U$ / V')
ax1.set_ylabel('光电流 $I$ / mA')
ax1.set_title('太阳能电池 I-U 特性曲线')
ax1.grid(alpha=0.3)
ax1.legend()

for i in range(4):
    ax2.plot(R_list[i], P_list[i], marks[i], color=colors[i], label=labels[i], linewidth=1.5, markersize=3)
ax2.set_xlabel('负载电阻 $R$ / $\Omega$')
ax2.set_ylabel('输出功率 $P$ / mW')
ax2.set_title('太阳能电池 R-P 特性曲线')
ax2.grid(alpha=0.3)
ax2.legend()
plt.tight_layout()

# ====================== 4. 图2：性能参数表图片 ======================
fig2, ax2_tab = plt.subplots(figsize=(10, 5), dpi=120)
ax2_tab.axis('off')

col_labels = ['参数', '第一组', '第二组', '第三组', '第四组']
row_labels = [
    '$P_{in}$/mW', '$P_{max}$/mW', '$U_0\\cdot I_s$/mW',
    '$R_{opt}$/$\Omega$', '$R_i$/$\Omega$', '$R_{opt}/R_i$',
    '$FF$', '$\eta$/%'
]
table_data = []
for i in range(len(row_labels)):
    row = [row_labels[i]]
    for j in range(4):
        row.append(f"{result_data[j][i]:.2f}")
    table_data.append(row)

tab2 = ax2_tab.table(cellText=table_data, colLabels=col_labels, cellLoc='center', loc='center')
tab2.auto_set_font_size(False)
tab2.set_fontsize(11)
tab2.scale(1, 2)
ax2_tab.set_title('表3.5.4 太阳能电池性能参数表', fontsize=14, pad=20)
plt.tight_layout()

# ====================== 5. 图3：原始U-I数据表格图片 ======================
fig3, ax3_tab = plt.subplots(figsize=(12, 6), dpi=120)
ax3_tab.axis('off')

# 构造原始数据表
raw_col = ['序号', 'U1(V)', 'I1(mA)', 'U2(V)', 'I2(mA)', 'U3(V)', 'I3(mA)', 'U4(V)', 'I4(mA)']
max_len = max(len(U1), len(U2), len(U3), len(U4))
raw_data = []

for n in range(max_len):
    row = [str(n+1)]
    row.append(f"{U1[n]:.2f}" if n<len(U1) else "-")
    row.append(f"{I1[n]:.2f}" if n<len(I1) else "-")
    row.append(f"{U2[n]:.2f}" if n<len(U2) else "-")
    row.append(f"{I2[n]:.2f}" if n<len(I2) else "-")
    row.append(f"{U3[n]:.2f}" if n<len(U3) else "-")
    row.append(f"{I3[n]:.2f}" if n<len(I3) else "-")
    row.append(f"{U4[n]:.2f}" if n<len(U4) else "-")
    row.append(f"{I4[n]:.2f}" if n<len(I4) else "-")
    raw_data.append(row)

tab3 = ax3_tab.table(cellText=raw_data, colLabels=raw_col, cellLoc='center', loc='center')
tab3.auto_set_font_size(False)
tab3.set_fontsize(9)
tab3.scale(1, 1.8)
ax3_tab.set_title('表3.5.2 太阳能电池原始U-I实验数据表', fontsize=14, pad=20)
plt.tight_layout()

# 显示所有窗口
plt.show()
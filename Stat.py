import csv
import math
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
Capital = 10000
l = 1
# Данные за 2 месяца, с шагом в 1 час
a = []
b = []
first_share = []
second_share = []
Axis = []


# Рассматриваемый период для вычеслений(количество измерений)
t = 22*13


# Коэффициент пропорциональности
k = []

Summ_first_share = 0
Summ_second_share = 0
Summ_k = 0

# Считываем файлы

with open('/home/velentina/Documents/diplom/SBER_200101_211201_1hour.csv', newline='') as File:
    reader = csv.reader(File, delimiter = ";")
    for row in reader:
        a.append(row)
with open('/home/velentina/Documents/diplom/SBERP_200101_211201_1_hour.csv', newline='') as File:
    reader = csv.reader(File, delimiter = ",")
    for row in reader:
        b.append(row)



# Преобразуем в списки
print('Преобразуем в списки')
for i in tqdm(range(len(a)-1)):
    first_share.append(float(a[i+1][4]))
    second_share.append(float(b[i+1][4]))
    k.append(second_share[i]/first_share[i])
    Summ_first_share = Summ_first_share+first_share[i]
    Summ_second_share = Summ_second_share+second_share[i]
    Axis.append(a[i+1][2])

# Корреляция, нормализация газпрома в данном случае по предудущему месяцу, спред
Delta_GR = 0
Delta_G2 = 0
Delta_R2 = 0
first_share_norm = []

k_summ = 0
for j in range(t):
    k_summ = k_summ + k[j]
k_srednee = k_summ / t
Spred=[]

print('Корреляция, нормализация')
for i in tqdm(range(len(first_share))):
    Delta_GR = Delta_GR + (first_share[i]- Summ_first_share/len(first_share))*(second_share[i]- Summ_second_share/len(second_share))
    Delta_G2 = Delta_G2 + (first_share[i]- Summ_first_share/len(first_share))**2
    Delta_R2 = Delta_R2 + (second_share[i]- Summ_second_share/len(second_share))**2
    if i > t-1:
        k_summ = 0
        for j in range(t):
            k_summ=k_summ+k[i-j]
        k_srednee = k_summ/t
    first_share_norm.append(first_share[i]*k_srednee)
    Spred.append(second_share[i] - first_share_norm[i])
cor = Delta_GR/((Delta_G2*Delta_R2)**0.5)
print(cor)

#  Считаем средний спред(пороговый) и "выполняем сделку"
summ_spred = 0
min_spred = 0
max_spred = 0
for j in range(t):
    summ_spred = summ_spred + math.fabs(Spred[j])
Sredn_spred = l*summ_spred/t



ind = 0
if second_share[1+t]-first_share_norm[1+t] < 0:
    ind = 1

# Mar = 0
#
# for i in range(len(ROSN)-t):
#     summ_spred = 0
#     min_spred = 0
#     max_spred = 0
#     for j in range(t):
#         if Spred[i+t-j] < 0 and Spred[i+t-j] < min_spred:
#             min_spred = Spred[i+t-j]
#             summ_spred = summ_spred +math.fabs(max_spred)
#             max_spred = 0
#         if Spred[i+t-j] > 0 and Spred[i+t-j] > max_spred:
#             max_spred = Spred[i+t-j]
#             summ_spred = summ_spred +math.fabs(min_spred)
#             min_spred = 0
#     Sredn_spred = summ_spred/t
#     if math.fabs(ROSN[i + t] - GAZP_norm[i + t]) > math.fabs(Sredn_spred) and (ROSN[i + t] - GAZP_norm[i + t]) > 0 and ind == 0:
#         Mar = Mar + math.fabs(ROSN[i + t] - GAZP_norm[i + t])/GAZP_norm[i+t]*100-0.1
#         ind = 1
#     if math.fabs(ROSN[i + t] - GAZP_norm[i + t]) > math.fabs(Sredn_spred) and (ROSN[i + t] - GAZP_norm[i + t]) < 0 and ind == 1:
#         Mar = Mar + math.fabs(ROSN[i + t] - GAZP_norm[i + t])/ROSN[i+t]*100-0.1
#         ind = 0
#
# print(Mar)




Sdel = []
N_r = 0
N_g = 0
Prib = Capital

print('Считаем средний спред(пороговый) и "выполняем сделку"')
for i in tqdm(range(len(second_share)-t)):
    summ_spred = 0
    for j in range(t):
        summ_spred = summ_spred + math.fabs(Spred[i+t-j])
    Sredn_spred = l*summ_spred/t
    if math.fabs(second_share[i+t]-first_share_norm[i+t])>math.fabs(Sredn_spred) and (second_share[i+t]-first_share_norm[i+t])>0 \
            and ind == 0 and math.fabs(second_share[i+t]-first_share_norm[i+t])/first_share[i+t] > 0.0007:
        Prib = Prib + N_r*second_share[i+t]*0.9995
        N_r = 0
        N_g = Prib//first_share[i+t]
        Prib = Prib - N_g*first_share[i+t]*1.0005
        ind = 1
        print(Axis[i+t],'Купили ',N_g,'шт. SBER по цене',first_share[i+t],', остаток = ',Prib,
              'стоимость портфеля =', Prib + N_g*first_share[i+t]*1.0005)
        Sdel.append(i+t)
    if math.fabs(second_share[i+t]-first_share_norm[i+t]) > math.fabs(Sredn_spred) and (second_share[i+t]-first_share_norm[i+t])<0 \
            and ind == 1 and math.fabs(second_share[i+t]-first_share_norm[i+t])/first_share[i+t] > 0.0007:
        Prib = Prib + N_g*first_share[i+t]*0.9995
        N_g = 0
        N_r = Prib//second_share[i+t]
        Prib = Prib - N_r*second_share[i+t]*1.0005
        ind = 0
        print(Axis[i+t],'Купили ',N_r,'шт. SBERP по цене',second_share[i + t],', остаток = ',Prib,
              'стоимость портфеля =', Prib + N_r*second_share[i+t]*1.0005)
        Sdel.append(i + t)

print('Стоимость портфеля', Prib + N_g * first_share[len(first_share)-1] * 0.9995 + N_r*second_share[len(second_share)-1]*0.9995)
Prib = (Prib + N_g * first_share[len(first_share)-1] * 0.9995 + N_r*second_share[len(second_share)-1]*0.9995-Capital)/Capital*100
print('Доходность портфеля при арбитраже', Prib, '%')
print('Доходность без арбитража', (-second_share[t]+second_share[len(first_share)-1])/second_share[t+1]*100, '%')

# строим график
Axis1 = []
for i in range(len(a)-1):
    Axis1.append(i)
plt.plot(Axis1,second_share, 'r--', label = 'first_share')
plt.plot(Axis1,first_share_norm, 'b--', label = 'second_share')
for i in range(len(Sdel)):
    plt.axvline(x=Sdel[i], color='green')
plt.legend()
plt.show()






# coding:utf
"""Пользователь вводит имя файла с изображением,
гистограммы которого нужно построить.
Строятся гистограммы по каждому из каналов, по яркости(Luminance), и RGB гистограмма.
Программа строит гистограммы и сохраняет в текущей папке.
Полученные гистограммы практически не отличаются от гистограмм,
полученных в коммерческих программах
Для работы программы необходим Python 2.7 с установленной PIL"""
from PIL import Image, ImageDraw # модули из PIL

def lum(c): #цвет пиксела RGB -> значение яркости
	#формула, которая обычно используется для определения яркости 
	return int(0.3*c[0] + 0.59*c[1] + 0.11*c[2])  
def r(c): #цвет пиксела RGB -> значение R
	return c[0]
def g(c): #цвет пиксела RGB -> значение G
	return c[1]
def b(c): #цвет пиксела RGB -> значение B
	return c[2]
def drawhist(hname, H, harr):
	""" Рисуем диаграмму, сохраняем в файл в текущую папку
	hname - имя файла
	H - высота рисунка
	harr - массив с высотами столбиков в гистограмме
	"""
	W = len(harr) #кол-во элементов массива
	hist = Image.new("RGB", (W, H), "white") #создаем рисунок в памяти
	draw = ImageDraw.Draw(hist) #объект для рисования на рисунке
	maxx = float(max(harr)) #высота самого высокого столбика
	if maxx == 0: #столбики равны 0
		draw.rectangle(((0, 0), (W, H)), fill="black")
	else:
		for i in range(W):
			draw.line(((i, H),(i, H-harr[i]/maxx*H)), fill="black") #рисуем столбики
	del draw #удаляем объект
	hist.save(hname) #сохраняем рисунок в файл

import os

def histo(dir_name,prefix,file_name):
    os.makedirs(dir_name, exist_ok=True)
    # список с функциями и префиксами названий файлов
    fnlist = [(lum, "luminosity_"), (r, "r_channel_"), (g, "g_channel_"), (b, "b_channel_")]
    # fname = input("input file name: ") #Ввод имени файла, гистограмму кот. нужно построить
    im = Image.open(file_name) #открываем файл
    # получаем список вида [(n1, c1), (n2, c2), ...], где
    # c - цвет пиксела в RGB
    # n - количество пикселов, имеющих данный цвет
    clrs = im.getcolors(im.size[0]*im.size[1])
    # ширина, высота гистограммы.
    # Ширину менять не стоит, т.к. все ф-и отображаются в [0..255]
    W, H = 256, 100
    hist_list = []
    for fn, hname in fnlist: #перебираем все функции
        harr = [0 for i in range(W)] #создаем массив [0, 0, 0, ...] длины W
        for n, c in clrs: #перебираем список созданный выше
            index = fn(c) #fn - отображение цвета в яркость или выделение цветового канала
            #индексы элементов массива показывают значения яркости и прочего. Диапазон [0..255]
            #значения элементов массива = количество пикселов с опред. значением яркости и т.д.
            harr[index] += n
        
        drawhist(dir_name + "/" + prefix + "_" + hname + "hist.png", H, harr) #рисуем гистограмму
        hist_list += [(hname + "hist",dir_name + "/" + prefix + "_" + hname + "hist.png")]
    # Нарисовали гистограммы по яркости и каналам, теперь
    # Рисуем гистограмму RGB
    rharr = [0 for i in range(W)]
    gharr = list(rharr)
    bharr = list(rharr)
    for n, c in clrs:
        rharr[r(c)] += n
        gharr[g(c)] += n
        bharr[b(c)] += n
    harr = [(rharr[i] + gharr[i] + bharr[i])/3 for i in range(W)]
    drawhist(dir_name + "/" + prefix + "_" + "RGB_hist.png", H, harr)
    hist_list += [("RGB_hist",dir_name + "/" + prefix + "_" + "RGB_hist.png")]
    return hist_list

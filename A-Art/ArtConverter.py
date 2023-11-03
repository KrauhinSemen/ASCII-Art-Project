import cv2
import pygame as pg
import os
from AsciiSorter import AsciiSorter


class ArtConverter:
    """Этот клас читает изображение и создаёт новое с помощью ASCII-символов"""

    def __init__(self, path, need_preview, font_size, ascii_palette, need_sort_palette, variable_space):
        """Конструктор класса"""
        # Проверка на наличие токого файла
        if not os.path.isfile(path):
            print("По данному пути ничего не найдено")
            exit()
        if "/" in path:
            print("Нежелательный символ '/' в пути, заменён на '\\'")
            path = path.replace("/", "\\")
        # Инициализация PyGame
        pg.init()
        # Путь до файла
        self.path = path
        self.need_preview = need_preview
        # Имя файла
        self.file_name = path.split("\\")[-1].split(".")[0]
        # Расширение файла
        self.expansion = path.split("\\")[-1].split(".")[1]
        # Получаем изображение как спсисок списков, состояших из номеров цвета пикселей
        self.image = self.get_image()
        # Получаем размеры изображения
        self.res = self.width, self.height = self.image.shape[0], self.image.shape[1]
        # Создание поля PyGame, на котором буде рисовать
        self.surface = pg.display.set_mode(self.res)
        # Палитра ascii-символов  (Можно поэксперементировать)
        self.ascii_chars = list(ascii_palette)
        # Обозначение пути до шрифта
        self.font_path = r"fonts\Roboto-BoldItalic.ttf"
        # Размер шрифта
        self.font_size = font_size
        # Добавление пробельного символа
        if variable_space:
            self.ascii_chars = [" "] + self.ascii_chars
        # Сортировка выбранной палитры ascii-символов
        if need_sort_palette:
            sorter = AsciiSorter(self.font_size, self.ascii_chars)
            self.ascii_chars = sorter.sort_ascii_chars()
        # Средство для определения, какой символ писать
        self.ascii_coefficient = 255 // (len(self.ascii_chars))
        # Определение шрифта для PyGame
        self.font = pg.font.SysFont(self.font_path, self.font_size)
        # Константа, взятая, чтобы размеры изображений совпадали (Можно поэксперементировать)
        self.char_step = int(self.font_size * 0.6)
        # Рендеринг символов, чтобы их можно было добавить в итоговое изображение
        self.rendered_ascii_chars = [self.font.render(char, False, "white") for char in self.ascii_chars]

    def get_image(self):
        """Этот метод переводит изображение в список списков пикслей"""
        # Получение изображения в виде высота-[ ширина-[ пиксель(3 цвета)-[],[],[] ],[ [][][] ],[ [][][] ] ]
        cv2_image = cv2.imread(self.path)
        # Транспонирование матрицы () иначе изображение перевёрнутое
        transposed_image = cv2.transpose(cv2_image)
        # Покраска пикселей в серый цвет (от 0 до 255 вроде бы)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def draw_converted_image(self):
        """Этот метод создаёт ASCII-изображение"""
        # Заполнение поля PyGame тёмным цветом
        self.surface.fill("black")
        # Выяснение какой сивол должен быть напечатан вместо конкретного пикселя (Можно поэксперементировать)
        char_indices = self.image // self.ascii_coefficient
        # Обход исходного изображение и добавления в итоговый результат ASCII-символы в зависимости от char_indices
        for x in range(0, self.width, self.char_step):
            for y in range(0, self.height, self.char_step):
                char_index = char_indices[x, y]
                self.surface.blit(self.rendered_ascii_chars[char_index], (x, y))

    def save_image(self):
        """Этот метод сохраняет изображение"""
        # Представление изображения PyGame, как список списков пикселей
        pygame_image = pg.surfarray.array3d(self.surface)
        # Транспонирование для работы с библиоекой CV2
        cv2_image = cv2.transpose(pygame_image)
        # Сохранение файла в папке "output_images"
        cv2.imwrite("output_images\\" + self.file_name + "_converted." + self.expansion, cv2_image)

    def run(self):
        """Этот метод запускает работу класса"""
        #  Начало рисовки
        self.draw_converted_image()
        if self.need_preview:
            # Обновление изображения PyGame
            pg.display.flip()
            # Вечный цикл для обработки ввода пользователя
            while True:
                for i in pg.event.get():
                    # Обработка закрытия программы
                    if i.type == pg.QUIT:
                        exit()
                    # Обработка нажатия клавиши "s"
                    elif i.type == pg.KEYDOWN:
                        if i.key == pg.K_s:
                            self.save_image()
        else:
            self.save_image()
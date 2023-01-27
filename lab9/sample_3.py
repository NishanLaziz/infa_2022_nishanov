class Dog:
    def __init__(self):
        self.angry = False

    def say_gaw(self):
        if self.angry:
            print('GAW-GAW')
        else:
            print('Gaw-gaw')

my_dog = Dog()
my_dog.say_gaw()      # ошибки нет, напечатает Gaw-gaw

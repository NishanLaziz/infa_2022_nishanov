class Dog:
    def say_gaw(self): # имя self для первого аргумента метода это общепринятое но не обязательное правило
        print('Gaw-gaw')

my_dog = Dog()
another_dog = Dog()
my_dog.say_gaw()      # вызовется функция Dog.say_gaw с параметром self = my_dog
another_dog.say_gaw()

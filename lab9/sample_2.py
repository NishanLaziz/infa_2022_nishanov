class Dog:
    def say_gaw(self):
        if self.angry:
            print('GAW-GAW')
        else:
            print('Gaw-gaw')

    def ping(self):
        self.angry = True

    def feed(self, food_count):
        if food_count > 10:
            self.angry = False

my_dog = Dog()
my_dog.feed(20)
my_dog.say_gaw()      # напечатает Gaw-gaw
my_dog.ping()
my_dog.say_gaw()      # напечатает GAW-GAW

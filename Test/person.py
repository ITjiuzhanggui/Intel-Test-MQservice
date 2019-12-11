from Test.bullet import Bullet


class Person(object):

    def __init__(self, gun):
        self.gun = gun

    def fire(self):  # 开火(开一枪子弹个数减一
        self.gun.shoot()

    def changeBox(self, count):  # 装几发子弹
        for i in range(count):
            self.gun.box.bullets.append(Bullet())
        self.gun.box.count = count
        print("换弹")

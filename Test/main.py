from Test.person import Person
from Test.gun import Gun
from Test.box import Box
from Test.bullet import Bullet


def main():
    bullets = [Bullet(), Bullet(), Bullet(), Bullet(), Bullet()]
    box = Box(bullets, 5)
    gun = Gun(box)
    per = Person(gun)

    per.fire()
    per.fire()
    per.fire()
    per.fire()
    per.fire()
    per.changeBox(5)
    per.fire()


if __name__ == '__main__':
    main()

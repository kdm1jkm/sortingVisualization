from enum import Enum
import pygame
import random
from typing import *
import sys

SIZE = (1280, 720)

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)


# Type of sorting algorithm
class SortType(Enum):
    BUBBLE_SORT = 1
    INSERTION_SORT = 2
    QUICK_SORT = 3


class SortingVisual:
    # initialize
    def __init__(self, init_list=None):
        self.sort_type: Optional[SortType] = None
        if init_list is None:
            init_list = []
        self.list: List = init_list
        self.i = self.j = self.left = self.right = self.begin = self.end = 0
        self.pivot = self.list[0]

    def shuffle(self):
        for i in range(len(self.list)):
            random_num = random.randrange(0, len(self.list))
            self.list[i], self.list[random_num] = self.list[random_num], self.list[i]

    def draw(self, screen: pygame.Surface, interval: int, default_color):
        color_dict = {
            SortType.BUBBLE_SORT: {self.i: RED, self.j: BLUE},
            SortType.INSERTION_SORT: {self.i: RED, self.j + 1: BLUE},
            SortType.QUICK_SORT: {self.left: RED, self.right: BLUE, self.list.index(self.pivot): GREEN}
        }.get(self.sort_type, {})
        w = SIZE[0] / len(self.list)
        for i in range(len(self.list)):
            pygame.draw.rect(screen, color_dict.get(i, default_color),
                             [i * w + interval, int(SIZE[1] * ((1 - self.ratio(i)) * 0.8 + 0.1)),
                              w - interval * 2, SIZE[1]])

    @property
    def max(self):
        result: int = self.list[0]
        for num in self.list:
            if num > result:
                result = num
        return result

    @property
    def min(self):
        result: int = self.list[0]
        for num in self.list:
            if num < result:
                result = num
        return result

    def ratio(self, index: int):
        num: int = self.list[index]
        result = (num - self.min) / (self.max - self.min)
        return result

    # Choose type of sorting algorithm and initialize for algorithm
    def init_sort(self, sort_type: SortType):
        self.sort_type = sort_type
        {
            SortType.BUBBLE_SORT: self.__init_bubble_sort,
            SortType.INSERTION_SORT: self.__init_insertion_sort,
            SortType.QUICK_SORT: self.__init_quick_sort
        }[sort_type]()

    def __init_bubble_sort(self):
        self.i = len(self.list)
        self.j = 0

    def __init_insertion_sort(self):
        self.i = 1
        self.j = 0
        self.key = self.list[1]

    def __init_quick_sort(self):
        self.left = 1
        self.right = 0
        self.begin = 0
        self.end = 0
        self.left_stack = [0]
        self.right_stack = [len(self.list) - 1]
        self.pivot = self.list[int(len(self.list) / 2)]

    # Process sorting one step
    def sort_next(self, fast_mode=False):
        r = {
            SortType.BUBBLE_SORT: self.__bubble_sort_next,
            SortType.INSERTION_SORT: self.__insertion_sort_next,
            SortType.QUICK_SORT: self.__quick_sort_next,
            None: False
        }[self.sort_type]
        if not r:
            return False
        r(fast_mode)
        return True

    def __bubble_sort_next(self, fast_mode: bool):
        if self.i < 0:
            self.sort_type = None
            return
        elif not self.j + 1 < self.i:
            self.j = 0
            self.i -= 1
            return
        if fast_mode:
            while self.j + 1 < self.i:
                if self.list[self.j] > self.list[self.j + 1]:
                    self.list[self.j], self.list[self.j + 1] \
                        = self.list[self.j + 1], self.list[self.j]
                self.j += 1
        else:
            if self.list[self.j] > self.list[self.j + 1]:
                self.list[self.j], self.list[self.j + 1] \
                    = self.list[self.j + 1], self.list[self.j]
            self.j += 1

    def __insertion_sort_next(self, fast_mode: bool):
        if not self.i < len(self.list):
            self.sort_type = None
            return
        elif not (self.list[self.j + 1] < self.list[self.j] and self.j >= 0):
            self.i += 1
            self.j = self.i - 1
            return

        if fast_mode:
            while self.list[self.j + 1] < self.list[self.j] and self.j >= 0:
                self.list[self.j + 1], self.list[self.j] = self.list[self.j], self.list[self.j + 1]
                self.j -= 1
        else:
            self.list[self.j + 1], self.list[self.j] = self.list[self.j], self.list[self.j + 1]
            self.j -= 1

    def __quick_sort_next(self, fast_mode: bool):
        if not self.left <= self.right:
            if self.left < self.end:
                self.left_stack.append(self.left)
                self.right_stack.append(self.end)
            if self.begin < self.right:
                self.left_stack.append(self.begin)
                self.right_stack.append(self.right)

            if len(self.left_stack) == 0:
                self.sort_type = None
                return

            self.begin = self.left = self.left_stack.pop()
            self.end = self.right = self.right_stack.pop()

            self.pivot = self.list[int((self.left + self.right) / 2)]
            return
        if fast_mode:
            while self.list[self.left] < self.pivot:
                self.left += 1
            while self.list[self.right] > self.pivot:
                self.right -= 1
            if self.left > self.right:
                return
            self.list[self.left], self.list[self.right] = self.list[self.right], self.list[self.left]
            self.left += 1
            self.right -= 1
        else:
            if self.list[self.left] < self.pivot:
                self.left += 1
            elif self.list[self.right] > self.pivot:
                self.right -= 1
            else:
                self.list[self.left], self.list[self.right] = self.list[self.right], self.list[self.left]
                self.left += 1
                self.right -= 1


def main():
    # Get data from user
    global SIZE
    SIZE = (int(input("Enter width>>")), int(input("Enter height>>")))
    length: int = int(input("Enter length>>"))

    if {
        "y": True,
        "n": False
    }.get(input("Manual input(y/n)>>"), False):
        ls = []
        for i in range(length):
            ls.append(int(input("Enter #%d>>" % (i + 1))))
    else:
        ls = list(range(length))

    fps: int = int(input("Enter fps>>"))

    s = SortingVisual(ls)

    if length > 200:
        interval = 0
    else:
        interval = 1

    # Initialize setting
    complete = False
    pause = False
    go_frame = False
    processed = False
    no_delay = False

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    while True:
        # check if no_delay mode
        if not no_delay:
            clock.tick(fps)

        # Handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if complete:
                        complete = False
                        s.shuffle()
                elif event.key == pygame.K_z:
                    s.init_sort(SortType.BUBBLE_SORT)
                    complete = False
                elif event.key == pygame.K_x:
                    s.init_sort(SortType.INSERTION_SORT)
                    complete = False
                elif event.key == pygame.K_c:
                    s.init_sort(SortType.QUICK_SORT)
                    complete = False
                elif event.key == pygame.K_SPACE:
                    pause = not pause
                elif event.key == pygame.K_p:
                    go_frame = True
                elif event.key == pygame.K_f:
                    no_delay = not no_delay

        # Check pause and run one frame
        if go_frame or not pause:
            go_frame = False
            processed = s.sort_next(no_delay)

        # Display if no_delay mode by using inverted color
        if no_delay:
            if pause:
                screen.fill(DARK_GRAY)
            else:
                screen.fill(BLACK)
            s.draw(screen, interval, WHITE)
        else:
            if pause:
                screen.fill(LIGHT_GRAY)
            else:
                screen.fill(WHITE)
            s.draw(screen, interval, BLACK)

        # Show list if shuffle or complete sorting
        if not complete and not processed:
            print(s.list)
        complete = not processed

        # Update screen
        pygame.display.flip()


if __name__ == '__main__':
    main()

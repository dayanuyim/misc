#!/bin/env python3
# -*- coding: utf-8 -*-

class Period:
    @property
    def begin(self):
        return self.__begin

    @property
    def end(self):
        return self.__end

    def __init__(self, begin, end):
        self.__begin = begin
        self.__end = end

    def contains(self, rhs):
        return self.begin <= rhs.begin and self.end >= rhs.end


class Movie:
    @property
    def name(self):
        return self.__name
    
    @property
    def period(self):
        return self.__period

    def __init__(self, name, period):
        self.__name = name
        self.__period = period

    def __str__(self):
        return "%s[%s~%s]" % (self.name, timeToStr(self.period.begin), timeToStr(self.period.end))

def strToTime(str):
    h, m = str.split(':')
    return 60 * int(h) + int(m)

def timeToStr(min):
    h = int(min/60)
    m = min - h * 60
    return "%02d:%02d" % (h, m)

def genMovies(name, duration, begins):
    movies = []
    for begin in begins:
        begin = strToTime(begin)
        m = Movie(name, Period(begin, begin + duration))
        movies.append(m)
    return movies

if __name__ == '__main__':
    movies = []
    movies.extend(genMovies("AnimalCity", 109, ("09:55", "13:35", "17:15", "20:55")))
    movies.extend(genMovies("LoveKill", 96, ("11:50", "15:30", "19:10", "22:50")))
    movies.extend(genMovies("KofuPanda", 95, ("10:25", "14:15", "20:45")))
    movies.extend(genMovies("HunderWinter", 114, ("12:00", "16:00", "22:30")))
    for m in movies:
        print(str(m))

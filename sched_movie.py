#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

'''
#設定 $PYTHONIOENCODING to 'utf-8', 或是 sys.stdout to 'utf8'
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

#測試
import os, locale, codecs
print(sys.stdout.encoding)
print(sys.stdout.isatty())
print(locale.getpreferredencoding())
print(sys.getfilesystemencoding())
print(os.environ["PYTHONIOENCODING"])
print(chr(246), chr(9786), chr(9787))
'''

# time(min) <-> string(HH:mm) =============
def strToTime(str):
    h, m = str.split(':')
    return 60 * int(h) + int(m)

def timeToStr(min):
    h = int(min/60)
    m = min - h * 60
    return "%02d:%02d" % (h, m)

# class ===================================
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

    def __str__(self):
        return "%s~%s" % (timeToStr(self.begin), timeToStr(self.end))

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

class Sched:
    def __init__(self, movie=None):
        self.__movies = []
        if movie is not None:   #init
            self.__movies.append(movie)

    def __str__(self):
        txts = [str(m) for m in movies]
        return "(" + ", ".join(txts) + ")"

    def put(self, movie):
        self.__movies.insert(0, movie)

    def hasMovie(self, name):
        for m in self.__movies:
            if m.name == name:
                return True
        return False

    def hasAllMovies(this, names):
        for name in names:
            if not this.hasMovie(name):
                return False
        return True

# Schedule Utils =========================
def getMoviesText(movies):
    txts = [str(m) for m in movies]
    return ", ".join(txts)

def schedHasMovie(sched, name):
    for m in sched:
        if m.name == name:
            return True
    return False

def schedHasMovies(sched, names):
    for name in names:
        if not schedHasMovie(sched, name):
            return False
    return True

def filterScheds(scheds, musts, min_movies):
    def cond(sched):
        return len(sched) >= min_movies and schedHasMovies(sched, musts)
    return [sched for sched in scheds if cond(sched)]

def printScheds(scheds):
    sn = 1
    for sched in scheds:
        print("%d: %s" % (sn, getMoviesText(sched)))
        sn += 1

# algo ==============================
def putMovieToScheds(movie, scheds):
    if not scheds:
        return [[movie]]

    for s in scheds:
        s.insert(0, movie)
    return scheds

# return scheds, which is the collection of sched
# a sched is a collection of movie
def pickMovies(period, movies):
    #print("pick '%s' in period '%s'" % (getMoviesText(movies), str(period)))

    #no schedule
    if not movies:
        return []

    #only movie
    if len(movies) == 1:
        m = movies[0]
        if period.contains(m.period):
            return [[m]]
        return []

    scheds = []
    target = movies[0]

    #pick the first movie
    if period.contains(target.period):
        #pick the rest 
        sub_movies = [m for m in movies if m.name != target.name]
        sub_period = Period(target.period.end, period.end)
        sub_scheds = pickMovies(sub_period, sub_movies)

        #rebuild schedule
        sub_scheds = putMovieToScheds(target, sub_scheds)
        scheds.extend(sub_scheds)

    # Or, not pick the first
    sub_movies = movies[1:]
    sub_scheds = pickMovies(period, sub_movies)
    scheds.extend(sub_scheds)

    return scheds

# utils ============================
def genMovies(name, duration, begins):
    movies = []
    for begin in begins:
        begin = strToTime(begin)
        m = Movie(name, Period(begin, begin + duration))
        movies.append(m)
    return movies

if __name__ == '__main__':
    if (sys.stdout.encoding is None):
        print("please set python env PYTHONIOENCODING=UTF-8, example: export PYTHONIOENCODING=UTF-8, when write to stdout.")

    # get movie
    movies = []
    movies.extend(genMovies("動物方程式", 109, ("09:55", "13:35", "17:15", "20:55")))
    movies.extend(genMovies("功夫熊貓3", 95, ("10:25", "14:15", "20:45")))
    movies.extend(genMovies("飛躍奇蹟", 106, ("10:25", "14:30", "18:35", "22:40")))
    movies.extend(genMovies("麥田書香", 90, ("13:15", "17:40", "22:05")))
    movies = sorted(movies, key=lambda m: m.period.begin)
    #for m in movies: print(str(m))

    scheds = pickMovies(Period(0, 24*60), movies)
    #scheds = filterScheds(scheds, {"動物方程式", "飛躍奇蹟"}, 2)
    scheds = filterScheds(scheds, {"動物方程式", "飛躍奇蹟"}, 2)
    printScheds(scheds)




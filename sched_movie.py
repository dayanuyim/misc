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
def strToMin(str):
    h, m = str.split(':')
    return 60 * int(h) + int(m)

def minToStr(min):
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
        return "%s~%s" % (minToStr(self.begin), minToStr(self.end))

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
        return "%s[%s]" % (self.name, str(self.period))

class Sched:
    def __init__(self, movie=None):
        self.__movies = []
        if movie is not None:   #init
            self.__movies.append(movie)

    def __str__(self):
        txts = [str(m) for m in self.__movies]
        return "(" + ", ".join(txts) + ")"

    def __len__(self):
        return len(self.__movies)

    def __iter__(self):
        return iter(self.__movies)

    def __getitem__(self, idx):
        return self.__movies[idx]

    def __setitem__(self, idx, val):
        self.__movies[idx] = val

    def __delitem__(self, idx):
        del self.__movies[idx]

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

def filterScheds(scheds, musts, min_movies):
    min_movies = max(min_movies, len(musts))
    def cond(sched):
        return len(sched) >= min_movies and sched.hasAllMovies(musts)
    return [sched for sched in scheds if cond(sched)]

def printScheds(scheds):
    sn = 1
    for sched in scheds:
        print("%d: %s" % (sn, str(sched)))
        sn += 1

# algo ==============================
def putMovieToScheds(scheds, movie):
    for s in scheds:
        s.put(movie)

# return scheds, which is the collection of sched
# a sched is a collection of movie
def pickMovies(period, movies):
    #print("pick '%s' in period '%s'" % (getMoviesText(movies), str(period)))

    #no schedule
    if not movies:
        return [Sched()]  #empty schedule

    #not pick the first
    sub_movies = movies[1:]
    scheds = pickMovies(period, sub_movies)

    #Or pick the first movie
    target = movies[0]
    if period.contains(target.period):
        #pick the rest 
        sub_movies = [m for m in movies if m.name != target.name]
        sub_period = Period(target.period.end, period.end)
        sub_scheds = pickMovies(sub_period, sub_movies)

        #rebuild schedule
        putMovieToScheds(sub_scheds, target)
        scheds.extend(sub_scheds)

    return scheds

# utils ============================
def genMovies(name, duration, begins):
    movies = []
    for begin in begins:
        begin = strToMin(begin)
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

    scheds = pickMovies(Period(0, 26*60), movies)
    scheds = filterScheds(scheds, {"動物方程式", "飛躍奇蹟"}, 4)
    printScheds(scheds)





# -*- coding: utf-8 -*-

one_to_nineteen = (u'ноль', u'один', u'два', u'три', u'четыре', u'пять',
                   u'шесть', u'семь', u'восемь', u'девять', u'десять',
                   u'одиннадцать', u'двенадцать', u'тринадцать',
                   u'четырнадцать', u'пятнадцать', u'шестнадцать',
                   u'семнадцать', u'восемнадцать', u'девятнадцать')

decs = ('', u'десять', u'двадцать', u'тридцать', u'сорок', u'пятьдесят',
        u'шестьдесят', u'семьдесят', u'восемьдесят', u'девяносто')

hundreds = ('', u'сто', u'двести', u'триста', u'четыреста',
            u'пятьсот', u'шестьсот', u'семьсот', u'восемьсот', u'девятьсот')

thousands = ('', u'одна тысяча', u'две тысячи',
             u'три тысячи', u'четыре тысячи')


def _one_convert(integer):
    return one_to_nineteen[integer]


def _two_convert(integer, string):
    if integer in range(20):
        result = one_to_nineteen[integer]

    else:
        result = decs[int(string[0])]

        if string[1] != '0':
            result = u'%s %s' % (result, one_to_nineteen[int(string[1])])

    return result


def convert(string):
    string = string.replace(' ', '').replace(',', '.')  # перенести
    string = str(string.split('.')[0])
    length = len(string)
    integer = int(string)

    if length == 1:
        result = _one_convert(integer)

    elif length == 2:
        result = _two_convert(integer, string)

    elif length == 3:
        result = hundreds[int(string[0])]

        tail = string[-2:]

        if tail != '00':
            result = u'%s %s' % (result, convert(tail))

    elif length in range(4, 7):
        tail = convert(string[-3:])

        str_head = string[:-3]
        int_head = int(str_head)

        if int_head in range(1, 5):
            head = thousands[int_head]

        else:
            head = u'%s тысяч' % (convert(str_head))

        result = u'%s %s' % (head, tail)

    else:
        result = ''

    return result.strip()

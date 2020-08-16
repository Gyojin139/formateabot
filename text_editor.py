import unicodedata
import string
from random import random, choice


class TextEditor:

    CIRCLED_UPPERCASE = 0x24B6
    CIRCLED_LOWERCASE = 0x24D0

    CURSIVE_UPPERCASE = 0x1D4D0
    CURSIVE_LOWERCASE = 0x1D4EA

    FRAKTUR_UPPERCASE = 0x1D56C
    FRAKTUR_LOWERCASE = 0x1D586

    DOUBLESTRUCK_UPPERCASE = 0x1D538
    DOUBLESTRUCK_LOWERCASE = 0x1D552

    SQUARED_UPPERCASE = 0x1F130
    SQUARED_LOWERCASE = SQUARED_UPPERCASE

    SANS_UPPERCASE = 0x1D5A0
    SANS_LOWERCASE = 0x1D5BA

    COMBINING = ''.join(chr(c) for c in range(0x0300, 0x0370) if c != 0x034f)

    @staticmethod
    def normalize(text):
        return unicodedata.normalize('NFKD', text)

    @classmethod
    def modifier(cls, text, uppercase_point, lowercase_point, exceptions={}):
        return ''.join(
            chr(exceptions[c]) if c in exceptions else
            chr(ord(c) - ord('A') + uppercase_point) if c in string.ascii_uppercase else
            chr(ord(c) - ord('a') + lowercase_point) if c in string.ascii_lowercase else
            c
            for c in cls.normalize(text)
        )

    @classmethod
    def cursive(cls, text):
        return cls.modifier(text, TextEditor.CURSIVE_UPPERCASE, TextEditor.CURSIVE_LOWERCASE)

    @classmethod
    def fraktur(cls, text):
        return cls.modifier(text, TextEditor.FRAKTUR_UPPERCASE, TextEditor.FRAKTUR_LOWERCASE)

    @classmethod
    def circled(cls, text):
        return cls.modifier(text, TextEditor.CIRCLED_UPPERCASE, TextEditor.CIRCLED_LOWERCASE)

    @classmethod
    def sans(cls, text):
        return cls.modifier(text, TextEditor.SANS_UPPERCASE, TextEditor.SANS_LOWERCASE)

    @classmethod
    def squared(cls, text):
        return cls.modifier(text, TextEditor.SQUARED_UPPERCASE, TextEditor.SQUARED_LOWERCASE)

    @classmethod
    def doublestruck(cls, text):
        exceptions = {
            'C': 0x2102,
            'H': 0x210D,
            'N': 0x2115,
            'P': 0x2119,
            'Q': 0x211A,
            'R': 0x211D,
            'Z': 0x2124,
        }
        return cls.modifier(text, TextEditor.DOUBLESTRUCK_UPPERCASE, TextEditor.DOUBLESTRUCK_LOWERCASE, exceptions)

    @classmethod
    def cursed(cls, text, level=6):
        if not text or level <= 0:
            return text
        out = [text[0]]
        i = 1
        while i < len(text):
            if random() > 1/level:
                out.append(choice(cls.COMBINING))
            else:
                out.append(text[i])
                i += 1
        return ''.join(out)


if __name__ == '__main__':
    text = 'sphinx of black qwartz judge my vow!'
    text = text + ' ' + text.upper()
    print(TextEditor.normalize(text))
    with open('fonts.txt', 'w', encoding='utf8') as f:
        print(TextEditor.cursive(text), file=f)
        print(TextEditor.fraktur(text), file=f)
        print(TextEditor.circled(text), file=f)
        print(TextEditor.doublestruck(text), file=f)
        print(TextEditor.sans(text), file=f)
        print(TextEditor.squared(text), file=f)
        print(TextEditor.cursed(text), file=f)

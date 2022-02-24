import re


class RegexException(Exception):
    pass

def regex_validator(aClass):
    def __setattr__(self, name, value):
        regexes = aClass.regexes
        if not name in regexes or re.search(regexes[name], value):
            self.__dict__[name] = value
        else:
            msg = f'Атрибут \"{name}\" класса \"{aClass.__name__}\"' \
                  f' не прошел валидацию.'
            raise RegexException(msg)
    aClass.__setattr__ = __setattr__
    return aClass

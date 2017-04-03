import json

from atod import settings
from atod.preprocessing.dictionary import get_types


def create_abilities_scheme():
    ''' Creates schema of abilities table.
    
        Raises:
            ValueError: if key contain 2 or more different types and
                they are not float and int.
    
        Returns:
            scheme (dict): keys - all properties in cleaned abilities,
                items - python
    '''

    with open(settings.ABILITIES_LISTS_FILE) as fp:
        skills = json.load(fp)

    keys_types = dict()
    for skill, description in skills.items():
        keys_types[skill] = get_types(description)

    key2type = dict()
    for skill, description in keys_types.items():
        for key, types in description.items():
            key2type.setdefault(key, set())
            key2type[key] = key2type[key].union(types)

    # if key contains both float and ints set types as float
    for key, types in key2type.items():
        # this is not the best way to check types, but for abilities
        # it's ok
        if int in types and float in types:
            key2type[key] = [float]

    for key, types in key2type.items():
        if len(types) > 1:
            raise ValueError('Single key maps to more than one type.')

    scheme = dict()
    for key, types in key2type.items():
        scheme[key] = settings.field_format[types.pop()]

    scheme['name'] = settings.field_format[str]
    scheme['HeroID'] = settings.field_format[int]
    scheme['lvl'] = settings.field_format[int]

    return scheme


if __name__ == '__main__':
    create_abilities_scheme()
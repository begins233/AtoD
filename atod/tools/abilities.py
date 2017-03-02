#!/usr/bin/env python3
''' Set of functions to work with npc_abilities.json'''
import os
import json

from atod import settings
# IDEA: move all from this import to this file
from atod.tools.json2vectors import (get_keys, make_flat_dict,
                                     find_heroes_abilities
                                     )


def count_keywords():
    with open(settings.ABILITIES_FILE, 'r') as fp:
        data = json.load(fp)['DOTAAbilities']

    heroes_abilities_list = find_heroes_abilities(data)

    heroes_abilities = {}
    for ability in heroes_abilities_list:
        heroes_abilities[ability] = data[ability]

    which_ability = create_which_ability(heroes_abilities)

    # print(json.dumps(heroes_abilities['life_stealer_feast'], indent=2))
    # print(sorted(which_ability['stun_duration']))

    label(heroes_abilities)


def label(abilities):
    print('LABEL')
    labels = {}
    for ability, parameters in abilities.items():
        labels[ability] = []
        parameters = make_flat_dict(parameters)
        for p in parameters.keys():
            if 'lifesteal' in p or 'vampiric' in p or 'leech' in p:
                labels[ability].append('stun')

    for ability, categories in labels.items():
        if len(categories) >= 1:
            print(ability)


def create_which_ability(abilities):
    ''' Creates mapping from effect to abilities where it occurs. '''
    which_ability = {}
    for ability, parameters in abilities.items():
        if isinstance(parameters, dict):
            flat_parameters = make_flat_dict(parameters)
        else:
            continue

        for p in flat_parameters.keys():
            try:
                which_ability[p].append(ability)
            except KeyError as e:
                which_ability[p] = [ability]

    return which_ability


if __name__ == '__main__':
    count_keywords()

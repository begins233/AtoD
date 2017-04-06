import json

from sqlalchemy.inspection import inspect

import atod.settings as settings
from atod.db import session
from atod.models import HeroModel
from atod.preprocessing.abilities import abilities as Abilities

mapper = inspect(HeroModel)

PRIMARIES = {
    'DOTA_ATTRIBUTE_AGILITY': 'agility',
    'DOTA_ATTRIBUTE_STRENGTH': 'strength',
    'DOTA_ATTRIBUTE_INTELLECT': 'intellect',
}


class Hero(object):
    ''' Interface for HeroModel. '''

    base_health = 200
    base_health_regen = 0.25
    base_mana = 50
    base_mana_regen = 0.01
    base_damage = 21
    base_armor = -1

    def __init__(self, name, lvl=1):
        ''' Create hero instance by id. '''
        # TODO: create metaclass to prevent changing this variables
        #       or just create properties
        self.lvl = lvl
        self.items = []
        self.talents = []

        # TODO: add names to database
        # load converter since there is no names in database
        with open(settings.CONVERTER) as fp:
            converter = json.load(fp)

        with open(settings.IN_GAME_CONVERTER) as fp:
            in_game_converter = json.load(fp)

        self.name = name
        self.id = converter[name]
        self.in_game_name = in_game_converter[str(self.id)]

        hero_data = session.query(HeroModel).filter(
            HeroModel.HeroID == self.id)[0]

        self.columns = [column.key for column in mapper.attrs]

        for column in self.columns:
            setattr(self, column, getattr(hero_data, column))

        # add roles dictionary
        self.roles = {}
        for role, lvl in zip(self.Role.split(','), self.Rolelevels.split(',')):
            self.roles[role] = int(lvl)

        self.primary = PRIMARIES[self.AttributePrimary]

        self.abilities = Abilities.filter(hero=self.in_game_name)

    # properties
    @property
    def str(self):
        return int(self.AttributeBaseStrength + \
                   (self.lvl - 1) * self.AttributeStrengthGain)

    @property
    def int(self):
        return int(self.AttributeBaseIntelligence + \
                   (self.lvl - 1) * self.AttributeAgilityGain)

    @property
    def agi(self):
        return int(self.AttributeBaseAgility + \
                   (self.lvl - 1) * self.AttributeAgilityGain)

    @property
    def health(self):
        return self.base_health + self.str * 20

    @property
    def health_regen(self):
        return self.base_health_regen + self.str * 0.03

    @property
    def mana(self):
        return self.int * 12

    @property
    def mana_regen(self):
        return self.int * 0.04

    @property
    def armor(self):
        return round(self.ArmorPhysical + self.agi / 7, 2)

    # TODO: this should be property with setter
    def abilities_labels(self):
        '''Returns dictionary ability->labels.'''
        labels = {}
        for a in self.abilities:
            labels[a.raw_name] = a.labels

        return labels

    def has(self, effect):
        for ability, labels in self.abilities_labels().items():
            if effect in labels:
                return True

        return False

    def __str__(self):
        return '<{name}, lvl={lvl}>'.format(name=self.name, lvl=self.lvl)

from os import listdir
from os.path import join

import toml

from src import category
from src.common import create_markup


class Candidata:
    def __init__(self, data_folder="./candidates"):
        self.cat_ids = set()
        self.categories = []
        self.cat_markup = {}
        self.index = {}
        self.markup = None
        self.names = []

        self.init(data_folder)
        self.get_candidates_keyboard()

    def init(self, data_folder):
        for filename in listdir(data_folder):
            with open(join(data_folder, filename), mode='r', encoding='utf-8') as candidate_file:
                self.read_file(candidate_file)
        self.names = list(self.index.keys())
        self.categories = list(map(category.humanize, self.cat_ids))

    def read_file(self, file):
        candidate = toml.loads(file.read())
        if not candidate['enabled']:
            return
        cand_name = candidate['name']
        del candidate['name']
        del candidate['enabled']
        self.index[cand_name] = candidate
        self.cat_ids.update(list(candidate.keys()))

    def get(self, cand, cat_name):
        cat = category.dehumanize(cat_name)
        return self.index[cand][cat]

    def get_candidates_keyboard(self):
        if not self.markup:
            self.markup = create_markup(self.names, shuffle=True)

        return self.markup

    def get_categories_keyboard(self, cand):
        if cand not in self.cat_markup:
            self.cat_markup[cand] = create_markup(list(map(category.humanize, self.index[cand].keys())))

        return self.cat_markup[cand]

    def get_categories_names(self):
        categories = list(map(lambda x: category.id_name_map[x], self.categories))
        return create_markup(categories)


data = Candidata()

from os import listdir
from os.path import join

import toml

import category
from common import create_markup


class Candidata:
    def __init__(self, data_folder="./candidates"):
        self.cand_name_id_map = {}
        self.cand_id_name_map = {}
        self.cat_ids = set()
        self.categories = []
        self.cat_markup = None
        self.index = {}
        self.markup = None
        self.names = []

        self.init(data_folder)

    def init(self, data_folder):
        for filename in listdir(data_folder):
            candidate_id = filename.split('.')[0]
            with open(join(data_folder, filename), mode='r', encoding='utf-8') as candidate_file:
                self.read_file(candidate_id, candidate_file)
        self.names = list(self.cand_name_id_map.keys())
        self.categories = list(map(category.humanize, self.cat_ids))

    def read_file(self, cand_id, file):
        candidate = toml.loads(file.read())
        self.cand_name_id_map[candidate['name']] = cand_id
        self.cand_id_name_map[cand_id] = candidate['name']
        del candidate['name']
        self.index[cand_id] = candidate
        self.cat_ids.update(list(candidate.keys()))

    def get(self, cand_name, cat_name):
        cand = self.dehumanize(cand_name)
        cat = category.dehumanize(cat_name)
        return self.index[cand][cat]

    def get_candidates_keyboard(self):
        if not self.markup:
            self.markup = create_markup(self.names)

        return self.markup

    def get_categories_keyboard(self):
        if not self.cat_markup:
            self.cat_markup = create_markup(self.categories)

        return self.cat_markup

    def get_categories_names(self):
        categories = list(map(lambda x: category.id_name_map[x], self.categories))
        return create_markup(categories)

    def humanize(self, cand_id):
        cand_name = self.cand_name_id_map[cand_id]
        return cand_name

    def dehumanize(self, cand_name):
        cand_id = self.cand_name_id_map[cand_name]
        return cand_id


data = Candidata()

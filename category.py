CONTACTS = 'contacts'
INTERVIEWS = 'interviews'
RU_CONTACTS = 'Контакты'
RU_INTERVIEWS = 'Интервью'

id_name_map_ru = {
    CONTACTS: RU_CONTACTS,
    INTERVIEWS: RU_INTERVIEWS
}
name_id_map_ru = {
    RU_CONTACTS: CONTACTS,
    RU_INTERVIEWS: INTERVIEWS
}


def humanize(cat_id):
    return id_name_map_ru[cat_id]


def dehumanize(cat_name):
    return name_id_map_ru[cat_name]

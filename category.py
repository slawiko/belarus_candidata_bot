CONTACTS_ID = 'contacts'
INTERVIEWS_ID = 'interviews'
CONTACTS_NAME = 'Кантакты'
INTERVIEWS_NAME = 'Інтэрв’ю'

id_name_map = {
    CONTACTS_ID: CONTACTS_NAME,
    INTERVIEWS_ID: INTERVIEWS_NAME
}
name_id_map = {
    CONTACTS_NAME: CONTACTS_ID,
    INTERVIEWS_NAME: INTERVIEWS_ID
}


def humanize(cat_id):
    return id_name_map[cat_id]


def dehumanize(cat_name):
    return name_id_map[cat_name]

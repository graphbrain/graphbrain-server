def has_gender_number(hg, actor, gender_number):
    gender_number_atom = '{}/p/.'.format(gender_number)
    return hg.exists((gender_number_atom, actor))


def gender_number(hg, actor):
    gender_numbers = {'female', 'male', 'group', 'non-human'}
    for gn in gender_numbers:
        if has_gender_number(hg, actor, gn):
            return gn
    return None


def actor_info(hg, actor):
    return {'gender_number': gender_number(hg, actor)}

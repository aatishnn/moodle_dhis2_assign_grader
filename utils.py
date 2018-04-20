def get_id_prompt(value_list, name_field):
    value_id = None
    valid_value_ids = []
    while not value_id:
        for c in value_list:
            valid_value_ids.append(c['id'])
            print("{}: {}".format(c['id'], c[name_field]))

        try:
            user_input = int(input("Enter ID:"))
        except ValueError:
            continue
        if user_input in valid_value_ids:
            value_id = user_input
    return value_id

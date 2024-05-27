def has_data_changed(existing_step, submitted_data):
    if not existing_step:
        return True
    for field_name, field_value in submitted_data.items():
        if field_name in [
            "csrfmiddlewaretoken",
            "problem_1",
            "p1name1",
            "p1age1",
            "p1comment1",
            "action",
        ]:
            continue
        existing_field = getattr(existing_step, field_name)
        if existing_field != field_value:
            return True
    return False
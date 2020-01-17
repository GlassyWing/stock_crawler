def convert_unit(value):
    """转换单位"""
    if value is None:
        return value

    if isinstance(value, str):
        try:
            unit = value[-1]
            if unit == '亿':
                value = float(value[:-1]) * 1e8
            elif unit == '万':
                value = float(value[:-1]) * 1e4
            elif unit == '千':
                value = float(value[:-1]) * 1e3
            else:
                value = float(value[:-1])
        except ValueError:
            pass

    return value

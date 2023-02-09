
def convert_refid_to_uuid(refid):
    """

    :param refid:
    :return:
    """
    uuid_dict = {
        'a': '10', 'b': '11', 'c': '12', 'd': '13',
        'e': '14', 'f': '15', 'g': '16', 'h': '17',
        'i': '18', 'k': '19', 'l': '20', 'm': '21',
        'n': '22', 'o': '23', 'p': '24', 'q': '25',
        'r': '26', 's': '27', 't': '28', 'u': '29',
        'v': '30', 'w': '31', 'x': '32', 'y': '33',
        'z': '34', '0': '00', '1': '01', '2': '02',
        '3': '03', '4': '04', '5': '05', '6': '06',
        '7': '07', '8': '08', '9': '09',
        'A': '30', 'B': '31', 'C': '32', 'D': '33',
        'E': '34', 'F': '35', 'G': '36', 'H': '37',
        'I': '38', 'K': '39', 'L': '40', 'M': '41',
        'N': '42', 'O': '43', 'P': '44', 'Q': '45',
        'R': '46', 'S': '47', 'T': '48', 'U': '49',
        'V': '50', 'W': '51', 'X': '52', 'Y': '53',
        'Z': '54'
    }

    uuid_str = ''

    for idchar in refid:
        uuid_str += uuid_dict[idchar]

    return uuid_str


def generate_uuid(refid):
    """

    :param refid:
    :return:
    """
    id_tok = refid.split('_')

    study_id = convert_refid_to_uuid(id_tok[0])
    series_id = None

    if len(id_tok) > 2:
        if id_tok[1] == 'cyto':
            series_id = '10' + convert_refid_to_uuid(id_tok[2])
        else:
            series_id = '10' + convert_refid_to_uuid('cbc')
    else:
        series_id = '10' + convert_refid_to_uuid('cbc')

    return study_id, series_id

def set_meta_data(dcm, i, j, value_type, newvalue):
    """

    :param dcm:
    :param i:
    :param j:
    :param value_type:
    :param newvalue:
    :return:
    """
    try:
        temp_data= get_meta_data(dcm, i, j)

        print(temp_data)

        if temp_data == False:
            dcm.add_new((i, j), value_type, newvalue)
        else:
            dcm[i, j].value = newvalue

        return dcm[i, j]

    except:
        return False

def get_meta_data(dcm, i, j):
    """

    :param dcm:
    :param i:
    :param j:
    :return:
    """
    try:
        return dcm[i, j]
    except:
        return False